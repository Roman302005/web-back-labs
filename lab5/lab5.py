from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import traceback
from werkzeug.security import check_password_hash, generate_password_hash
import os
from os import path

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

def db_connect():
    db_type = current_app.config.get('DB_TYPE', 'postgres')
    
    if db_type == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='roma',
            user='roma',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        db_path = '/home/Roman303030/web-back-labs/database.db'
        
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
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
            
            conn.commit()
            
        except Exception as e:
            print(f"Ошибка подключения к SQLite: {e}")
            raise
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def execute_query(cur, query, params):
    db_type = current_app.config.get('DB_TYPE', 'postgres')
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
    
    try:
        conn, cur = db_connect()
        
        execute_query(cur, "SELECT login FROM users WHERE login=?;", (login,))
        existing_user = cur.fetchone()
        
        if existing_user:
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')
        
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
    
    try:
        conn, cur = db_connect()
        
        execute_query(cur, "SELECT * FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        user_password = user['password']
        
        if not check_password_hash(user_password, password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['login'] = login
        session['user_id'] = user['id']
        db_close(conn, cur)
        
        return render_template('lab5/success_login.html', login=login)
    
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
    
    try:
        conn, cur = db_connect()
        
        execute_query(cur, "SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        user_id = user['id']
        
        execute_query(cur, "INSERT INTO articles (user_id, title, article_text, is_public) VALUES (?, ?, ?, ?);", 
                     (user_id, title, article_text, True))
        
        db_close(conn, cur)
        return redirect('/lab5')
    
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
        
        execute_query(cur, "SELECT * FROM articles WHERE user_id=?;", (user_id,))
        articles = cur.fetchall()
        
        db_close(conn, cur)
        return render_template('lab5/articles.html', articles=articles, login=login)
    
    except Exception as e:
        print(f"Ошибка при загрузке статей: {e}")
        traceback.print_exc()
        return render_template('lab5/articles.html', articles=[], error=f'Ошибка при загрузке статей: {str(e)}')