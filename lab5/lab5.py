from flask import Blueprint, render_template, request, session, redirect, url_for
import psycopg2
import traceback
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

# Функции для работы с БД
def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='roma',
        user='roma',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

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
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')
        
        # Добавляем пользователя
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))
        
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
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        if user['password'] != password:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        # Сохраняем логин в сессии
        session['login'] = login
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
    return redirect(url_for('lab5.lab'))