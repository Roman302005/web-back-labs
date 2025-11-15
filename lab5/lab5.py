from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import traceback
from werkzeug.security import check_password_hash, generate_password_hash
import os
from os import path

# Импорты для разных БД
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    pass

try:
    import sqlite3
except ImportError:
    pass

lab5 = Blueprint('lab5', __name__)

# Функции для работы с БД
def db_connect():
    db_type = current_app.config.get('DB_TYPE', 'postgres')
    
    if db_type == 'postgres':
        # PostgreSQL подключение
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='roma',
            user='roma',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # SQLite подключение
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Для доступа к полям по имени как в PostgreSQL
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def execute_query(cur, query, params):
    """Универсальная функция выполнения запроса для разных БД"""
    db_type = current_app.config.get('DB_TYPE', 'postgres')
    if db_type == 'postgres':
        cur.execute(query.replace('?', '%s'), params)
    else:
        cur.execute(query, params)

# Главная страница лабораторной работы 5
@lab5.route('/lab5')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

# Регистрация пользователей
@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    try:
        conn, cur = db_connect()
        
        # Проверяем существование пользователя
        execute_query(cur, "SELECT login FROM users WHERE login=?;", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')
        
        password_hash = generate_password_hash(password)
        
        # Добавляем пользователя
        execute_query(cur, "INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
        
        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()
        return render_template('lab5/register.html', error=f'Ошибка при регистрации: {str(e)}')

# Аутентификация (вход в систему)
@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')
    
    try:
        conn, cur = db_connect()
        
        # Ищем пользователя в БД
        execute_query(cur, "SELECT * FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        # Для SQLite получаем данные по-разному
        if current_app.config.get('DB_TYPE') == 'postgres':
            user_password = user['password']
        else:
            user_password = user['password']
        
        if not check_password_hash(user_password, password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['login'] = login
        session['user_id'] = user['id'] if 'id' in user else user[0]
        db_close(conn, cur)
        
        return render_template('lab5/success_login.html', login=login)
    
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()
        return render_template('lab5/login.html', error=f'Ошибка при входе: {str(e)}')

# Выход из системы
@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    return redirect(url_for('lab5.lab'))

# Создание статьи
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    
    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля')
    
    try:
        conn, cur = db_connect()
        
        # Получаем ID пользователя
        execute_query(cur, "SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        user_id = user['id'] if 'id' in user else user[0]
        
        # Вставляем статью в базу
        execute_query(cur, "INSERT INTO articles (user_id, title, article_text, is_public) VALUES (?, ?, ?, ?);", 
                     (user_id, title, article_text, True))
        
        db_close(conn, cur)
        return redirect('/lab5')
    
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()
        return render_template('lab5/create_article.html', error=f'Ошибка при создании статьи: {str(e)}')

# Список статей пользователя
@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    try:
        conn, cur = db_connect()
        
        # Получаем ID пользователя
        execute_query(cur, "SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        user_id = user['id'] if 'id' in user else user[0]
        
        # Получаем все статьи пользователя
        execute_query(cur, "SELECT * FROM articles WHERE user_id=?;", (user_id,))
        articles = cur.fetchall()
        
        db_close(conn, cur)
        return render_template('lab5/articles.html', articles=articles, login=login)
    
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()
        return render_template('lab5/articles.html', articles=[], error=f'Ошибка при загрузке статей: {str(e)}')