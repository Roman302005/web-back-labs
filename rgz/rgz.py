from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
import traceback
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import re

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    pass

try:
    import sqlite3
except ImportError:
    pass

rgz = Blueprint('rgz', __name__)

def validate_login(login):
    """Валидация логина: только латинские буквы, цифры и знаки препинания"""
    if not login or len(login.strip()) == 0:
        return False, "Логин не может быть пустым"
    
    if len(login) < 3:
        return False, "Логин должен содержать минимум 3 символа"
    
    if len(login) > 30:
        return False, "Логин не может быть длиннее 30 символов"
    
    # Разрешаем латинские буквы, цифры, дефисы, подчеркивания
    if not re.match(r'^[a-zA-Z0-9_-]+$', login):
        return False, "Логин может содержать только латинские буквы, цифры, дефисы и подчеркивания"
    
    return True, ""

def validate_password(password):
    """Валидация пароля"""
    if not password or len(password.strip()) == 0:
        return False, "Пароль не может быть пустым"
    
    if len(password) < 4:
        return False, "Пароль должен содержать минимум 4 символа"
    
    if len(password) > 50:
        return False, "Пароль не может быть длиннее 50 символов"
    
    return True, ""

def db_connect():
    db_type = current_app.config.get('DB_TYPE', 'sqlite')
    
    if db_type == 'postgres':
        try:
            conn = psycopg2.connect(
                host='127.0.0.1',
                database='roma',
                user='roma',
                password='123'
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
            return conn, cur
        except Exception as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")
            print("Переключаемся на SQLite")
            db_type = 'sqlite'
    
    # Используем SQLite
    import os
    from os import path
    db_path = path.join(path.dirname(path.abspath(__file__)), '..', 'database.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Создаем таблицы для сообщений если их нет
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rgz_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user VARCHAR(30) NOT NULL,
                to_user VARCHAR(30) NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_by_sender BOOLEAN DEFAULT 0,
                deleted_by_receiver BOOLEAN DEFAULT 0
            )
        """)
        
        conn.commit()
        return conn, cur
        
    except Exception as e:
        print(f"Ошибка подключения к SQLite: {e}")
        raise

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def execute_query(cur, query, params):
    db_type = current_app.config.get('DB_TYPE', 'sqlite')
    if db_type == 'postgres':
        cur.execute(query.replace('?', '%s'), params)
    else:
        cur.execute(query, params)

def get_current_user():
    return session.get('login')

def is_admin():
    return get_current_user() == 'admin'

def get_all_users():
    """Получить всех пользователей из БД"""
    try:
        conn, cur = db_connect()
        current_user = get_current_user()
        
        execute_query(cur, "SELECT login FROM users WHERE login != ?;", (current_user,))
        
        users = [row['login'] for row in cur.fetchall()]
        db_close(conn, cur)
        return users
    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")
        return []

def get_chat_messages(user1, user2):
    """Получить сообщения между двумя пользователями"""
    try:
        conn, cur = db_connect()
        execute_query(cur, """
            SELECT * FROM rgz_messages 
            WHERE ((from_user = ? AND to_user = ?) OR (from_user = ? AND to_user = ?))
            AND ((from_user = ? AND deleted_by_sender = 0) OR (to_user = ? AND deleted_by_receiver = 0))
            ORDER BY timestamp;
        """, (user1, user2, user2, user1, user1, user1))
        
        messages = []
        for row in cur.fetchall():
            messages.append(dict(row))
        
        db_close(conn, cur)
        return messages
    except Exception as e:
        print(f"Ошибка при получении сообщений: {e}")
        return []

@rgz.route('/rgz')
def main():
    login = get_current_user()
    if not login:
        return render_template('rgz/rgz.html')
    
    users = get_all_users()
    
    return render_template('rgz/rgz.html', 
                         login=login, 
                         users=users,
                         users_count=len(users),
                         is_admin=is_admin())

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    return redirect('/lab5/register')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    return redirect('/lab5/login')

@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)
    flash('Вы вышли из системы', 'info')
    return redirect('/rgz')

@rgz.route('/rgz/delete_account', methods=['GET', 'POST'])
def delete_account():
    current_user = get_current_user()
    if not current_user:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('rgz/delete_account.html')
    
    # Подтверждение удаления
    confirm = request.form.get('confirm')
    if confirm != 'DELETE':
        flash('Для удаления аккаунта необходимо ввести слово DELETE', 'error')
        return render_template('rgz/delete_account.html')
    
    try:
        conn, cur = db_connect()
        
        # Удаляем пользователя
        execute_query(cur, "DELETE FROM users WHERE login = ?;", (current_user,))
        
        # Удаляем все сообщения пользователя
        execute_query(cur, "DELETE FROM rgz_messages WHERE from_user = ? OR to_user = ?;", (current_user, current_user))
        
        # Удаляем статьи пользователя (если есть таблица articles)
        try:
            execute_query(cur, "DELETE FROM articles WHERE user_id IN (SELECT id FROM users WHERE login = ?);", (current_user,))
        except:
            pass  # Игнорируем ошибку если таблицы articles нет
        
        db_close(conn, cur)
        
        # Выходим из системы
        session.pop('login', None)
        flash('Ваш аккаунт успешно удален', 'success')
        return redirect('/rgz')
        
    except Exception as e:
        print(f"Ошибка при удалении аккаунта: {e}")
        flash('Ошибка при удалении аккаунта', 'error')
        return render_template('rgz/delete_account.html')

@rgz.route('/rgz/chat/<username>')
def chat(username):
    current_user = get_current_user()
    if not current_user:
        return redirect('/lab5/login')
    
    # Проверяем существование пользователя
    try:
        conn, cur = db_connect()
        execute_query(cur, "SELECT login FROM users WHERE login = ?;", (username,))
        user_exists = cur.fetchone()
        db_close(conn, cur)
        
        if not user_exists:
            flash('Пользователь не найден', 'error')
            return redirect('/rgz')
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        flash('Ошибка при загрузке чата', 'error')
        return redirect('/rgz')
    
    chat_messages = get_chat_messages(current_user, username)
    return render_template('rgz/chat.html', 
                         login=current_user, 
                         chat_with=username, 
                         messages=chat_messages)

@rgz.route('/rgz/send_message', methods=['POST'])
def send_message():
    current_user = get_current_user()
    if not current_user:
        return redirect('/lab5/login')
    
    to_user = request.form.get('to_user')
    message_text = request.form.get('message')
    
    if not to_user or not message_text:
        flash('Заполните все поля', 'error')
        return redirect(f'/rgz/chat/{to_user}')
    
    # Валидация сообщения
    if len(message_text.strip()) == 0:
        flash('Сообщение не может быть пустым', 'error')
        return redirect(f'/rgz/chat/{to_user}')
    
    if len(message_text) > 1000:
        flash('Сообщение слишком длинное', 'error')
        return redirect(f'/rgz/chat/{to_user}')
    
    # Запрещаем отправку сообщений администратору
    if to_user == 'admin':
        flash('Нельзя отправлять сообщения администратору', 'error')
        return redirect('/rgz')
    
    # Сохраняем сообщение в БД
    try:
        conn, cur = db_connect()
        execute_query(cur, """
            INSERT INTO rgz_messages (from_user, to_user, message) 
            VALUES (?, ?, ?);
        """, (current_user, to_user, message_text))
        
        db_close(conn, cur)
        flash('Сообщение отправлено!', 'success')
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        flash('Ошибка при отправке сообщения', 'error')
    
    return redirect(f'/rgz/chat/{to_user}')

@rgz.route('/rgz/delete_message/<int:message_id>')
def delete_message(message_id):
    current_user = get_current_user()
    if not current_user:
        return redirect('/lab5/login')
    
    try:
        conn, cur = db_connect()
        
        # Получаем информацию о сообщении
        execute_query(cur, "SELECT * FROM rgz_messages WHERE id = ?;", (message_id,))
        message = cur.fetchone()
        
        if not message:
            flash('Сообщение не найдено', 'error')
            return redirect('/rgz')
        
        message_dict = dict(message)
        
        # Определяем, кто удаляет сообщение
        if message_dict['from_user'] == current_user:
            # Удаляем для отправителя
            execute_query(cur, "UPDATE rgz_messages SET deleted_by_sender = 1 WHERE id = ?;", (message_id,))
            redirect_user = message_dict['to_user']
        elif message_dict['to_user'] == current_user:
            # Удаляем для получателя
            execute_query(cur, "UPDATE rgz_messages SET deleted_by_receiver = 1 WHERE id = ?;", (message_id,))
            redirect_user = message_dict['from_user']
        else:
            flash('Нет прав для удаления этого сообщения', 'error')
            return redirect('/rgz')
        
        # Если сообщение удалено обоими пользователями, удаляем полностью
        execute_query(cur, """
            DELETE FROM rgz_messages 
            WHERE id = ? AND deleted_by_sender = 1 AND deleted_by_receiver = 1;
        """, (message_id,))
        
        db_close(conn, cur)
        flash('Сообщение удалено', 'success')
        return redirect(f'/rgz/chat/{redirect_user}')
        
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")
        flash('Ошибка при удалении сообщения', 'error')
        return redirect('/rgz')

@rgz.route('/rgz/admin/delete_user/<username>')
def delete_user(username):
    if not is_admin():
        flash('Доступ запрещен', 'error')
        return redirect('/rgz')
    
    if username == 'admin':
        flash('Нельзя удалить администратора', 'error')
        return redirect('/rgz')
    
    try:
        conn, cur = db_connect()
        
        # Удаляем пользователя
        execute_query(cur, "DELETE FROM users WHERE login = ?;", (username,))
        
        # Удаляем все сообщения пользователя
        execute_query(cur, "DELETE FROM rgz_messages WHERE from_user = ? OR to_user = ?;", (username, username))
        
        db_close(conn, cur)
        flash(f'Пользователь {username} удален', 'success')
        
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")
        flash('Ошибка при удалении пользователя', 'error')
    
    return redirect('/rgz')

@rgz.route('/rgz/admin/edit_user/<username>', methods=['GET', 'POST'])
def edit_user(username):
    if not is_admin():
        flash('Доступ запрещен', 'error')
        return redirect('/rgz')
    
    if request.method == 'GET':
        return render_template('rgz/edit_user.html', user_login=username)
    
    new_password = request.form.get('password')
    
    # Валидация пароля
    is_valid, error_msg = validate_password(new_password)
    if not is_valid:
        flash(error_msg, 'error')
        return render_template('rgz/edit_user.html', user_login=username)
    
    try:
        conn, cur = db_connect()
        execute_query(cur, "UPDATE users SET password = ? WHERE login = ?;", 
                     (generate_password_hash(new_password), username))
        db_close(conn, cur)
        flash('Пароль пользователя изменен', 'success')
    except Exception as e:
        print(f"Ошибка при изменении пароля: {e}")
        flash('Ошибка при изменении пароля', 'error')
    
    return redirect('/rgz')