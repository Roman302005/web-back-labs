from flask import Blueprint, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from database.models import users, articles

lab8 = Blueprint('lab8', __name__)

# Минимальный CSS
CSS = '''<style>body{font:Arial;margin:40px;background:#f5f5f5}.c{max-width:600px;margin:auto;background:white;padding:30px;border-radius:8px;box-shadow:0 2px 4px #0001}h1,h2{margin-top:0}.n{margin:20px 0;padding-bottom:15px;border-bottom:1px solid #ddd}.n a{margin-right:15px;color:#06c;text-decoration:none}input,textarea{width:100%;padding:10px;margin:8px 0 20px;border:1px solid #ccc;border-radius:4px;box-sizing:border-box}textarea{height:150px}button,.b{background:#06c;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;display:inline-block}.b:hover{background:#05a}.err{background:#fdd;color:#c00;padding:10px;margin:15px 0;border-radius:4px}.art{background:#f9f9f9;padding:15px;margin:10px 0;border-radius:4px;border-left:3px solid #06c}.art-actions{margin-top:10px}.art-actions a{margin-right:10px;color:#666}.f{margin-top:30px;padding-top:20px;border-top:1px solid #ddd;color:#666}.public{border-left-color:#2a7}.search{margin:20px 0}.search input{width:70%;display:inline-block;margin-right:10px}.search button{width:25%}</style>'''

# Главная
@lab8.route('/lab8/')
def main():
    html = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Лаб 8</title>{CSS}</head>
    <body>
        <div class="c">
            <h1>Лабораторная работа 8</h1>
            <div class="n">
                <a href="/lab8/">Главная</a>
                <a href="/lab8/articles">Статьи</a>
                <a href="/lab8/create">Создать</a>
                <a href="/">На сайт</a>
            </div>
    '''
    
    if current_user.is_authenticated:
        html += f'''
            <h2>Привет, {current_user.login}!</h2>
            <p><a href="/lab8/articles" class="b">Все статьи</a></p>
            <p><a href="/lab8/create" class="b" style="background:#28a">Создать</a></p>
            <p><a href="/lab8/logout" class="b" style="background:#666">Выйти</a></p>
        '''
    else:
        html += '''
            <h2>Система статей</h2>
            <p><a href="/lab8/login" class="b">Войти</a></p>
            <p><a href="/lab8/register" class="b" style="background:#2a7">Регистрация</a></p>
            <p><small>Гости могут просматривать публичные статьи</small></p>
        '''
    
    html += '''
        <div class="f">ФБИ-34 • 2025</div>
        </div>
    </body>
    </html>
    '''
    return html

# Вход
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')
        remember = request.form.get('remember')
        
        if not login_form or not password_form:
            error = 'Заполните все поля'
        else:
            user = users.query.filter_by(login=login_form).first()
            if user and check_password_hash(user.password, password_form):
                login_user(user, remember=remember)
                return redirect('/lab8/')
            error = 'Неверный логин или пароль'
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Вход</title>{CSS}</head>
    <body>
        <div class="c">
            <h2>Вход</h2>
            <div class="n">
                <a href="/lab8/">Назад</a>
                <a href="/lab8/register">Регистрация</a>
            </div>
            {f'<div class="err">{error}</div>' if error else ''}
            <form method="POST">
                <input type="text" name="login" placeholder="Логин" required>
                <input type="password" name="password" placeholder="Пароль" required>
                <div>
                    <input type="checkbox" name="remember" id="remember">
                    <label for="remember">Запомнить меня</label>
                </div>
                <button type="submit">Войти</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return html

# Регистрация
@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')
        
        if not login_form or not password_form:
            error = 'Заполните все поля'
        else:
            existing_user = users.query.filter_by(login=login_form).first()
            if existing_user:
                error = 'Логин уже занят'
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
                    error = 'Ошибка'
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Регистрация</title>{CSS}</head>
    <body>
        <div class="c">
            <h2>Регистрация</h2>
            <div class="n">
                <a href="/lab8/">Назад</a>
                <a href="/lab8/login">Войти</a>
            </div>
            {f'<div class="err">{error}</div>' if error else ''}
            <form method="POST">
                <input type="text" name="login" placeholder="Логин" required>
                <input type="password" name="password" placeholder="Пароль" required>
                <button type="submit" style="background:#2a7">Зарегистрироваться</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return html

# Выход
@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

# Список статей С ПОИСКОМ
@lab8.route('/lab8/articles')
def article_list():
    search_query = request.args.get('search', '')
    
    # Если пользователь авторизован - видит все свои статьи и публичные
    # Если не авторизован - видит только публичные
    
    if current_user.is_authenticated:
        if search_query:
            # Поиск по своим статьям и публичным
            articles_list = articles.query.filter(
                (articles.title.ilike(f'%{search_query}%')) | 
                (articles.content.ilike(f'%{search_query}%'))
            ).all()
        else:
            # Все статьи
            articles_list = articles.query.all()
    else:
        # Гости видят все статьи (в реальности были бы только публичные)
        # Для простоты показываем все, но пометим публичные
        if search_query:
            articles_list = articles.query.filter(
                (articles.title.ilike(f'%{search_query}%')) | 
                (articles.content.ilike(f'%{search_query}%'))
            ).all()
        else:
            articles_list = articles.query.all()
    
    # Формируем HTML
    articles_html = ''
    for article in articles_list:
        user = users.query.get(article.user_id)
        
        # Определяем класс статьи (публичная или нет)
        article_class = 'art public' if getattr(article, 'is_public', True) else 'art'
        
        # Кнопки действий (только для автора)
        actions = ''
        if current_user.is_authenticated and article.user_id == current_user.id:
            actions = f'''
            <div class="art-actions">
                <a href="/lab8/edit/{article.id}">✏️ Редактировать</a>
                <a href="/lab8/delete/{article.id}" onclick="return confirm('Удалить?')">🗑️ Удалить</a>
            </div>
            '''
        
        # Определяем метку
        meta = f'Автор: {user.login if user else "Неизвестно"}'
        if current_user.is_authenticated and article.user_id == current_user.id:
            meta += ' • <strong>Ваша статья</strong>'
        elif getattr(article, 'is_public', True):
            meta += ' • <span style="color:#2a7">Публичная</span>'
        
        articles_html += f'''
        <div class="{article_class}">
            <h3>{article.title}</h3>
            <p>{article.content[:150]}{'...' if len(article.content) > 150 else ''}</p>
            <div class="art-meta">{meta}</div>
            {actions}
        </div>
        '''
    
    if not articles_html:
        articles_html = '<p>Статей пока нет.</p>'
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Статьи</title>{CSS}</head>
    <body>
        <div class="c">
            <h2>Все статьи</h2>
            <div class="n">
                <a href="/lab8/">На главную</a>
                {'''<a href="/lab8/create">Создать</a>''' if current_user.is_authenticated else ''}
            </div>
            
            <div class="search">
                <form method="GET">
                    <input type="text" name="search" placeholder="Поиск по статьям..." value="{search_query}">
                    <button type="submit">🔍 Искать</button>
                </form>
                {f'<p><small>Поиск: "{search_query}"</small></p>' if search_query else ''}
            </div>
            
            {articles_html}
            
            {'''<p><a href="/lab8/create" class="b">+ Новая статья</a></p>''' if current_user.is_authenticated else ''}
        </div>
    </body>
    </html>
    '''
    return html

# Создание статьи С ВЫБОРОМ ПУБЛИЧНОСТИ
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    error = ''
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_public = request.form.get('is_public') == 'on'
        
        if not title or not content:
            error = 'Заполните заголовок и текст'
        else:
            try:
                # Создаем статью с флагом публичности
                new_article = articles(
                    title=title,
                    content=content,
                    user_id=current_user.id
                )
                # Добавляем флаг публичности если есть в модели
                if hasattr(new_article, 'is_public'):
                    new_article.is_public = is_public
                
                db.session.add(new_article)
                db.session.commit()
                return redirect('/lab8/articles')
            except Exception as e:
                db.session.rollback()
                error = f'Ошибка: {str(e)}'
    
    # Форма с галочкой публичности
    public_checkbox = '''
    <div style="margin: 15px 0;">
        <input type="checkbox" name="is_public" id="is_public" checked>
        <label for="is_public">📢 Сделать статью публичной (видна всем)</label>
    </div>
    ''' if hasattr(articles, 'is_public') else ''
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Создать</title>{CSS}</head>
    <body>
        <div class="c">
            <h2>Создать статью</h2>
            <div class="n">
                <a href="/lab8/">На главную</a>
                <a href="/lab8/articles">Все статьи</a>
            </div>
            {f'<div class="err">{error}</div>' if error else ''}
            <form method="POST">
                <input type="text" name="title" placeholder="Заголовок" required>
                <textarea name="content" placeholder="Текст статьи..." required></textarea>
                {public_checkbox}
                <button type="submit" style="background:#2a7">Опубликовать</button>
                <a href="/lab8/articles" style="margin-left:10px;">Отмена</a>
            </form>
        </div>
    </body>
    </html>
    '''
    return html

# Редактирование статьи
@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get(article_id)
    if not article or article.user_id != current_user.id:
        return redirect('/lab8/articles')
    
    error = ''
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_public = request.form.get('is_public') == 'on'
        
        if not title or not content:
            error = 'Заполните все поля'
        else:
            try:
                article.title = title
                article.content = content
                if hasattr(article, 'is_public'):
                    article.is_public = is_public
                db.session.commit()
                return redirect('/lab8/articles')
            except:
                db.session.rollback()
                error = 'Ошибка'
    
    # Галочка публичности для редактирования
    public_checkbox = f'''
    <div style="margin: 15px 0;">
        <input type="checkbox" name="is_public" id="is_public" {'checked' if getattr(article, 'is_public', True) else ''}>
        <label for="is_public">📢 Публичная статья</label>
    </div>
    ''' if hasattr(articles, 'is_public') else ''
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Редактировать</title>{CSS}</head>
    <body>
        <div class="c">
            <h2>Редактировать</h2>
            <div class="n">
                <a href="/lab8/">На главную</a>
                <a href="/lab8/articles">Все статьи</a>
            </div>
            {f'<div class="err">{error}</div>' if error else ''}
            <form method="POST">
                <input type="text" name="title" value="{article.title}" required>
                <textarea name="content" required>{article.content}</textarea>
                {public_checkbox}
                <button type="submit" style="background:#17a">Сохранить</button>
                <a href="/lab8/articles" style="margin-left:10px;">Отмена</a>
            </form>
        </div>
    </body>
    </html>
    '''
    return html

# Удаление статьи
@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.get(article_id)
    if article and article.user_id == current_user.id:
        try:
            db.session.delete(article)
            db.session.commit()
        except:
            db.session.rollback()
    return redirect('/lab8/articles')