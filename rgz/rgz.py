from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import traceback
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

rgz = Blueprint('rgz', __name__)

# Имитация базы данных в памяти
users_db = {}
messages_db = []
admin_login = "admin"  # Логин администратора

def init_db():
    # Создаем администратора по умолчанию
    if admin_login not in users_db:
        users_db[admin_login] = {
            'password': generate_password_hash('admin123'),
            'is_admin': True
        }
    
    # Добавляем тестовых пользователей для демонстрации
    test_users = [
        {'login': 'alex', 'password': '123'},
        {'login': 'maria', 'password': '123'},
        {'login': 'ivan', 'password': '123'}
    ]
    
    for user in test_users:
        if user['login'] not in users_db:
            users_db[user['login']] = {
                'password': generate_password_hash(user['password']),
                'is_admin': False
            }

init_db()

def get_current_user():
    return session.get('login')

def is_admin():
    return get_current_user() == admin_login

def get_user_messages(username):
    """Получить все сообщения пользователя (входящие и исходящие)"""
    user_messages = []
    for msg in messages_db:
        if msg['to_user'] == username or msg['from_user'] == username:
            user_messages.append(msg)
    return user_messages

def get_chat_messages(user1, user2):
    """Получить сообщения между двумя пользователями"""
    chat_messages = []
    for msg in messages_db:
        if (msg['from_user'] == user1 and msg['to_user'] == user2) or \
           (msg['from_user'] == user2 and msg['to_user'] == user1):
            chat_messages.append(msg)
    return sorted(chat_messages, key=lambda x: x['timestamp'])

@rgz.route('/rgz')
def main():
    login = get_current_user()
    if not login:
        return render_template('rgz/rgz.html')
    
    # Для отладки - выводим всех пользователей в консоль
    print("Все пользователи в системе:", list(users_db.keys()))
    print("Текущий пользователь:", login)
    
    # Для обычных пользователей - список пользователей
    if not is_admin():
        # Показываем всех пользователей кроме текущего
        other_users = [user for user in users_db.keys() if user != login]
        print("Пользователи для отображения:", other_users)
        
        return render_template('rgz/rgz.html', 
                             login=login, 
                             users=other_users,
                             users_db_size=len(users_db),
                             all_users=list(users_db.keys()))
    
    # Для администратора - управление пользователями
    return render_template('rgz/rgz.html', 
                         login=login, 
                         users=users_db, 
                         is_admin=True,
                         users_db_size=len(users_db),
                         all_users=list(users_db.keys()))

# Остальные функции остаются без изменений...
@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not login or not password:
        flash('Заполните все поля', 'error')
        return render_template('rgz/register.html')
    
    if login in users_db:
        flash('Пользователь с таким логином уже существует', 'error')
        return render_template('rgz/register.html')
    
    # Регистрируем нового пользователя
    users_db[login] = {
        'password': generate_password_hash(password),
        'is_admin': False
    }
    
    flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
    return redirect('/rgz/login')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not login or not password:
        flash('Заполните все поля', 'error')
        return render_template('rgz/login.html')
    
    if login not in users_db:
        flash('Неверный логин или пароль', 'error')
        return render_template('rgz/login.html')
    
    user_data = users_db[login]
    if not check_password_hash(user_data['password'], password):
        flash('Неверный логин или пароль', 'error')
        return render_template('rgz/login.html')
    
    session['login'] = login
    flash('Вы успешно вошли в систему!', 'success')
    return redirect('/rgz')

@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)
    flash('Вы вышли из системы', 'info')
    return redirect('/rgz')

@rgz.route('/rgz/chat/<username>')
def chat(username):
    current_user = get_current_user()
    if not current_user:
        return redirect('/rgz/login')
    
    if username not in users_db:
        flash('Пользователь не найден', 'error')
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
        return redirect('/rgz/login')
    
    to_user = request.form.get('to_user')
    message_text = request.form.get('message')
    
    if not to_user or not message_text:
        flash('Заполните все поля', 'error')
        return redirect(f'/rgz/chat/{to_user}')
    
    if to_user not in users_db:
        flash('Пользователь не найден', 'error')
        return redirect('/rgz')
    
    # Сохраняем сообщение
    messages_db.append({
        'id': len(messages_db) + 1,
        'from_user': current_user,
        'to_user': to_user,
        'message': message_text,
        'timestamp': datetime.now(),
        'deleted_by_sender': False,
        'deleted_by_receiver': False
    })
    
    flash('Сообщение отправлено!', 'success')
    return redirect(f'/rgz/chat/{to_user}')

@rgz.route('/rgz/delete_message/<int:message_id>')
def delete_message(message_id):
    current_user = get_current_user()
    if not current_user:
        return redirect('/rgz/login')
    
    # Находим сообщение
    for msg in messages_db:
        if msg['id'] == message_id:
            # Проверяем права на удаление
            if msg['from_user'] == current_user:
                msg['deleted_by_sender'] = True
            elif msg['to_user'] == current_user:
                msg['deleted_by_receiver'] = True
            
            # Если сообщение удалено обоими пользователями, удаляем полностью
            if msg['deleted_by_sender'] and msg['deleted_by_receiver']:
                messages_db.remove(msg)
            
            flash('Сообщение удалено', 'success')
            return redirect(f'/rgz/chat/{msg["to_user"] if msg["from_user"] == current_user else msg["from_user"]}')
    
    flash('Сообщение не найдено', 'error')
    return redirect('/rgz')

@rgz.route('/rgz/admin/delete_user/<username>')
def delete_user(username):
    if not is_admin():
        flash('Доступ запрещен', 'error')
        return redirect('/rgz')
    
    if username == admin_login:
        flash('Нельзя удалить администратора', 'error')
        return redirect('/rgz')
    
    if username in users_db:
        # Удаляем пользователя и все его сообщения
        del users_db[username]
        global messages_db
        messages_db = [msg for msg in messages_db if msg['from_user'] != username and msg['to_user'] != username]
        flash(f'Пользователь {username} удален', 'success')
    
    return redirect('/rgz')

@rgz.route('/rgz/admin/edit_user/<username>', methods=['GET', 'POST'])
def edit_user(username):
    if not is_admin():
        flash('Доступ запрещен', 'error')
        return redirect('/rgz')
    
    if username not in users_db:
        flash('Пользователь не найден', 'error')
        return redirect('/rgz')
    
    if request.method == 'GET':
        return render_template('rgz/edit_user.html', user_login=username)
    
    new_password = request.form.get('password')
    if not new_password:
        flash('Введите новый пароль', 'error')
        return render_template('rgz/edit_user.html', user_login=username)
    
    users_db[username]['password'] = generate_password_hash(new_password)
    flash('Пароль пользователя изменен', 'success')
    return redirect('/rgz')