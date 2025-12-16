from flask import Blueprint, render_template, jsonify, abort, request, redirect, url_for, session, flash, make_response, g
import sqlite3
import os

lab8 = Blueprint('lab8', __name__)

# Конфигурация базы данных
DATABASE = 'lab8.db'

def get_db():
    """Получение соединения с базой данных"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    """Закрытие соединения с базой данных"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Инициализация базы данных"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    
    # Создание таблицы пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT
    )
    ''')
    
    # Создание таблицы статей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    db.commit()
    db.close()

# Инициализация базы данных при первом запуске
if not os.path.exists(DATABASE):
    init_db()

@lab8.before_request
def before_request():
    """Установка соединения с БД перед каждым запросом"""
    g.db = get_db()

# Главная страница лабораторной
@lab8.route('/lab8/')
def main():
    username = session.get('username', 'Anonymous')
    return render_template('lab8/lab8.html', username=username)

# Вход
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                      (username, password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = username
            session['user_id'] = user['id']
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('lab8.main'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('lab8/login.html')

# Регистрация
@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        cursor = g.db.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                          (username, password, email))
            g.db.commit()
            
            session['username'] = username
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            session['user_id'] = user['id']
            
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('lab8.main'))
        except sqlite3.IntegrityError:
            flash('Пользователь с таким именем уже существует', 'error')
    
    return render_template('lab8/register.html')

# Выход
@lab8.route('/lab8/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('lab8.main'))

# Список статей
@lab8.route('/lab8/articles')
def articles():
    cursor = g.db.cursor()
    
    cursor.execute('''
    SELECT articles.*, users.username 
    FROM articles 
    LEFT JOIN users ON articles.user_id = users.id 
    ORDER BY articles.created_at DESC
    ''')
    articles_list = cursor.fetchall()
    
    return render_template('lab8/articles.html', articles=articles_list)

# Создание статьи
@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create_article():
    if 'username' not in session or session['username'] == 'Anonymous':
        flash('Для создания статьи необходимо войти в систему', 'error')
        return redirect(url_for('lab8.login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('user_id')
        
        if title and content:
            cursor = g.db.cursor()
            cursor.execute('INSERT INTO articles (title, content, user_id) VALUES (?, ?, ?)',
                          (title, content, user_id))
            g.db.commit()
            flash('Статья успешно создана!', 'success')
            return redirect(url_for('lab8.articles'))
        else:
            flash('Заполните все поля', 'error')
    
    return render_template('lab8/create.html')

# Удаление статьи
@lab8.route('/lab8/delete/<int:article_id>')
def delete_article(article_id):
    if 'username' not in session:
        return redirect(url_for('lab8.login'))
    
    cursor = g.db.cursor()
    
    # Проверяем, принадлежит ли статья текущему пользователю
    cursor.execute('SELECT user_id FROM articles WHERE id = ?', (article_id,))
    article = cursor.fetchone()
    
    if article and article['user_id'] == session.get('user_id'):
        cursor.execute('DELETE FROM articles WHERE id = ?', (article_id,))
        g.db.commit()
        flash('Статья удалена', 'success')
    
    return redirect(url_for('lab8.articles'))