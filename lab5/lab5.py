from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import traceback
from werkzeug.security import check_password_hash, generate_password_hash
import os
from os import path
import re

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    pass
# sdfsdf ывапыва 
try:
    import sqlite3
except ImportError:
    pass

lab5 = Blueprint('lab5', __name__)

def validate_login(login):
    """Валидация логина: только латинские буквы, цифры и разрешенные символы"""
    if not login or len(login.strip()) == 0:
        return False, "Логин не может быть пустым"
    
    if len(login) < 3:
        return False, "Логин должен содержать минимум 3 символа"
    
    if len(login) > 30:
        return False, "Логин не может быть длиннее 30 символов"
    
    # Разрешаем латинские буквы, цифры, дефисы, подчеркивания, точки
    if not re.match(r'^[a-zA-Z0-9_.-]+$', login):
        return False, "Логин может содержать только латинские буквы, цифры, точки, дефисы и подчеркивания"
    
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

def validate_article_data(title, article_text):
    """Валидация данных статьи"""
    if not title or len(title.strip()) == 0:
        return False, "Название статьи не может быть пустым"
    
    if not article_text or len(article_text.strip()) == 0:
        return False, "Текст статьи не может быть пустым"
    
    if len(title) > 50:
        return False, "Название статьи не может быть длиннее 50 символов"
    
    if len(article_text) > 5000:
        return False, "Текст статьи не может быть длиннее 5000 символов"
    
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
    db_path = path.join(path.dirname(path.abspath(__file__)), '..', 'database.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Создаем таблицы если их нет
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login VARCHAR(30) UNIQUE NOT NULL,
                password VARCHAR(200) NOT NULL
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title VARCHAR(50),
                article_text TEXT,
                is_favorite BOOLEAN DEFAULT 0,
                is_public BOOLEAN DEFAULT 1,
                likes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Создаем администратора если его нет
        cur.execute("SELECT * FROM users WHERE login = 'admin';")
        admin_exists = cur.fetchone()
        
        if not admin_exists:
            cur.execute(
                "INSERT INTO users (login, password) VALUES (?, ?);",
                ('admin', generate_password_hash('admin123'))
            )
            print("Администратор 'admin' создан с паролем 'admin123'")
        
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

@lab5.route('/lab5')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    # Валидация логина
    is_valid, error_msg = validate_login(login)
    if not is_valid:
        return render_template('lab5/register.html', error=error_msg)
    
    # Валидация пароля
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        return render_template('lab5/register.html', error=error_msg)
    
    try:
        conn, cur = db_connect()
        
        execute_query(cur, "SELECT login FROM users WHERE login=?;", (login,))
        existing_user = cur.fetchone()
        
        if existing_user:
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')
        
        # Хешируем пароль с солью
        password_hash = generate_password_hash(password)
        
        execute_query(cur, "INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
        
        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
        traceback.print_exc()
        return render_template('lab5/register.html', error=f'Ошибка при регистрации: {str(e)}')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')
    
    # Валидация логина
    is_valid, error_msg = validate_login(login)
    if not is_valid:
        return render_template('lab5/login.html', error=error_msg)
    
    try:
        conn, cur = db_connect()
        
        execute_query(cur, "SELECT * FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        user_password = user['password']
        
        # Проверяем пароль с помощью check_password_hash
        if not check_password_hash(user_password, password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['login'] = login
        session['user_id'] = user['id']
        db_close(conn, cur)
        
        # Перенаправляем на RGZ вместо lab5
        return redirect('/rgz')
    
    except Exception as e:
        print(f"Ошибка при входе: {e}")
        traceback.print_exc()
        return render_template('lab5/login.html', error=f'Ошибка при входе: {str(e)}')

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    return redirect(url_for('lab5.lab'))

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
    
    # Валидация данных статьи
    is_valid, error_msg = validate_article_data(title, article_text)
    if not is_valid:
        return render_template('lab5/create_article.html', error=error_msg)
    
    try:
        conn, cur = db_connect()
        
        execute_query(cur, "SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        user_id = user['id']
        
        execute_query(cur, "INSERT INTO articles (user_id, title, article_text, is_public) VALUES (?, ?, ?, ?);", 
                     (user_id, title, article_text, True))
        
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        print(f"Ошибка при создании статьи: {e}")
        traceback.print_exc()
        return render_template('lab5/create_article.html', error=f'Ошибка при создании статьи: {str(e)}')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    try:
        conn, cur = db_connect()
        
        execute_query(cur, "SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        user_id = user['id']
        
        execute_query(cur, "SELECT * FROM articles WHERE user_id=? ORDER BY created_at DESC;", (user_id,))
        articles = cur.fetchall()
        
        db_close(conn, cur)
        return render_template('lab5/articles.html', articles=articles, login=login)
    
    except Exception as e:
        print(f"Ошибка при загрузке статей: {e}")
        traceback.print_exc()
        return render_template('lab5/articles.html', articles=[], error=f'Ошибка при загрузке статей: {str(e)}')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    try:
        conn, cur = db_connect()
        
        execute_query(cur, "SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        user_id = user['id']
        
        if request.method == 'GET':
            execute_query(cur, "SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
            article = cur.fetchone()
            
            if not article:
                db_close(conn, cur)
                return redirect('/lab5/list')
            
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article=article)
        
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        
        if not (title and article_text):
            return render_template('lab5/edit_article.html', 
                                 article={'id': article_id, 'title': title, 'article_text': article_text}, 
                                 error='Заполните все поля')
        
        # Валидация данных статьи
        is_valid, error_msg = validate_article_data(title, article_text)
        if not is_valid:
            return render_template('lab5/edit_article.html',
                                 article={'id': article_id, 'title': title, 'article_text': article_text},
                                 error=error_msg)
        
        execute_query(cur, "UPDATE articles SET title=?, article_text=? WHERE id=? AND user_id=?;", 
                     (title, article_text, article_id, user_id))
        
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        print(f"Ошибка при редактировании статьи: {e}")
        traceback.print_exc()
        return render_template('lab5/edit_article.html', error=f'Ошибка при редактировании статьи: {str(e)}')

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    try:
        conn, cur = db_connect()
        
        execute_query(cur, "SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        user_id = user['id']
        
        execute_query(cur, "DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
        
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        print(f"Ошибка при удалении статьи: {e}")
        traceback.print_exc()
        return redirect('/lab5/list')

@lab5.route('/lab5/delete_account', methods=['GET', 'POST'])
def delete_account():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/delete_account.html')
    
    # Подтверждение удаления
    confirm = request.form.get('confirm')
    if confirm != 'DELETE':
        return render_template('lab5/delete_account.html', error='Для удаления аккаунта необходимо ввести слово DELETE')
    
    try:
        conn, cur = db_connect()
        
        # Получаем ID пользователя
        execute_query(cur, "SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/delete_account.html', error='Пользователь не найден')
        
        user_id = user['id']
        
        # Удаляем статьи пользователя
        execute_query(cur, "DELETE FROM articles WHERE user_id=?;", (user_id,))
        
        # Удаляем пользователя
        execute_query(cur, "DELETE FROM users WHERE id=?;", (user_id,))
        
        db_close(conn, cur)
        
        # Выходим из системы
        session.pop('login', None)
        session.pop('user_id', None)
        
        return render_template('lab5/delete_success.html')
        
    except Exception as e:
        print(f"Ошибка при удалении аккаунта: {e}")
        traceback.print_exc()
        return render_template('lab5/delete_account.html', error=f'Ошибка при удалении аккаунта: {str(e)}')