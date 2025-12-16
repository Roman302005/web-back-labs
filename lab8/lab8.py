from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from database.models import users, articles

lab8 = Blueprint('lab8', __name__)

# Функция для создания базового HTML с CSS
def render_lab8_page(title, content):
    return f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="/static/lab8.css">
    </head>
    <body>
        <div class="container">
            <header class="header">
                <h1>Лабораторная работа 8</h1>
                <p>Система управления статьями</p>
            </header>
            
            <nav class="nav">
                <a href="/lab8/">Главная</a>
                <a href="/lab8/articles/">Статьи</a>
                <a href="/lab8/create/">Создать</a>
                <a href="/">На сайт</a>
            </nav>
            
            <div class="content">
                {content}
            </div>
            
            <footer class="footer">
                <p>Лелюх Роман • ФБИ-34 • 2025</p>
            </footer>
        </div>
    </body>
    </html>
    '''

# Главная страница
@lab8.route('/lab8/')
def main():
    if current_user.is_authenticated:
        content = f'''
        <div class="welcome">
            <h2>Добро пожаловать, {current_user.login}!</h2>
            <p>Вы успешно авторизовались в системе</p>
            <div class="links">
                <a href="/lab8/articles/" class="btn">Просмотреть статьи</a>
                <a href="/lab8/create/" class="btn btn-success">Создать статью</a>
                <a href="/lab8/logout" class="btn btn-outline">Выйти</a>
            </div>
        </div>
        '''
    else:
        content = '''
        <div class="welcome">
            <h2>Система управления статьями</h2>
            <p>Для работы с системой необходимо авторизоваться</p>
            <div class="links">
                <a href="/lab8/login" class="btn">Войти</a>
                <a href="/lab8/register" class="btn btn-success">Регистрация</a>
            </div>
        </div>
        '''
    
    return render_lab8_page("Главная", content)

# Вход
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')
        
        if not login_form or not password_form:
            error = 'Заполните все поля'
        else:
            user = users.query.filter_by(login=login_form).first()
            if user and check_password_hash(user.password, password_form):
                login_user(user, remember=False)
                return redirect('/lab8/')
            else:
                error = 'Неверный логин или пароль'
    
    content = f'''
    <h2>Вход в систему</h2>
    {f'<div class="alert alert-error">{error}</div>' if error else ''}
    
    <form method="POST">
        <div class="form-group">
            <label>Логин:</label>
            <input type="text" name="login" required>
        </div>
        
        <div class="form-group">
            <label>Пароль:</label>
            <input type="password" name="password" required>
        </div>
        
        <button type="submit" class="btn btn-block">Войти</button>
    </form>
    
    <div class="text-center mt-20">
        <p>Нет аккаунта? <a href="/lab8/register">Зарегистрируйтесь</a></p>
    </div>
    '''
    
    return render_lab8_page("Вход", content)

# Регистрация
@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    error = None
    
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')
        
        if not login_form or not password_form:
            error = 'Заполните все поля'
        else:
            existing_user = users.query.filter_by(login=login_form).first()
            if existing_user:
                error = 'Пользователь с таким логином уже существует'
            else:
                hashed_password = generate_password_hash(password_form)
                try:
                    new_user = users(login=login_form, password=hashed_password)
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user, remember=False)
                    return redirect('/lab8/')
                except:
                    db.session.rollback()
                    error = 'Ошибка при регистрации'
    
    content = f'''
    <h2>Регистрация</h2>
    {f'<div class="alert alert-error">{error}</div>' if error else ''}
    
    <form method="POST">
        <div class="form-group">
            <label>Логин:</label>
            <input type="text" name="login" required>
        </div>
        
        <div class="form-group">
            <label>Пароль:</label>
            <input type="password" name="password" required>
        </div>
        
        <button type="submit" class="btn btn-block btn-success">Зарегистрироваться</button>
    </form>
    
    <div class="text-center mt-20">
        <p>Уже есть аккаунт? <a href="/lab8/login">Войдите</a></p>
    </div>
    '''
    
    return render_lab8_page("Регистрация", content)

# Выход
@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

# Список статей
@lab8.route('/lab8/articles/')
@login_required
def article_list():
    articles_list = articles.query.all()
    
    if articles_list:
        articles_html = ''
        for article in articles_list:
            user = users.query.get(article.user_id)
            delete_btn = ''
            if article.user_id == current_user.id:
                delete_btn = f'<a href="/lab8/delete/{article.id}" class="btn btn-danger" style="padding: 5px 10px; font-size: 14px;" onclick="return confirm(\'Удалить статью?\')">Удалить</a>'
            
            articles_html += f'''
            <div class="card">
                <h3 class="card-title">{article.title}</h3>
                <div class="card-content">
                    {article.content[:200]}{'...' if len(article.content) > 200 else ''}
                </div>
                <div class="card-meta">
                    <span>Автор: {user.login if user else 'Неизвестно'}</span>
                    {delete_btn}
                </div>
            </div>
            '''
    else:
        articles_html = '<div class="alert alert-info">Статей пока нет. Будьте первым!</div>'
    
    content = f'''
    <h2>Все статьи</h2>
    <div class="mb-20">
        <a href="/lab8/create/" class="btn">+ Новая статья</a>
    </div>
    
    {articles_html}
    '''
    
    return render_lab8_page("Статьи", content)

# Создание статьи
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    error = None
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('article_text')
        
        if title and content:
            try:
                new_article = articles(
                    title=title,
                    content=content,
                    user_id=current_user.id
                )
                db.session.add(new_article)
                db.session.commit()
                return redirect('/lab8/articles/')
            except Exception as e:
                db.session.rollback()
                error = f'Ошибка: {str(e)}'
        else:
            error = 'Заполните все поля'
    
    content = f'''
    <h2>Создать статью</h2>
    {f'<div class="alert alert-error">{error}</div>' if error else ''}
    
    <form method="POST">
        <div class="form-group">
            <label>Заголовок:</label>
            <input type="text" name="title" placeholder="Введите заголовок" required>
        </div>
        
        <div class="form-group">
            <label>Текст статьи:</label>
            <textarea name="article_text" placeholder="Напишите вашу статью..." required></textarea>
        </div>
        
        <div class="links">
            <button type="submit" class="btn btn-success">Опубликовать</button>
            <a href="/lab8/articles/" class="btn btn-outline">Отмена</a>
        </div>
    </form>
    '''
    
    return render_lab8_page("Создание статьи", content)

# Удаление статьи
@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.get(article_id)
    
    if article and article.user_id == current_user.id:
        db.session.delete(article)
        db.session.commit()
    
    return redirect('/lab8/articles/')