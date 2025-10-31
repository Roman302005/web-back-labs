from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
from collections import deque

request_log = deque(maxlen=20)

lab1= Blueprint('lab1', __name__)




@lab1.route('/index')
def index():
    return """<!doctype html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            header {
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #2c3e50;
            }
            h1 {
                color: #2c3e50;
                margin: 0;
            }
            .menu {
                margin: 30px 0;
            }
            .menu a {
                display: block;
                padding: 15px;
                margin: 10px 0;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s ease;
            }
            .menu a:hover {
                background: #2980b9;
            }
            .home-link {
                display: inline-block;
                padding: 10px 20px;
                background: #2c3e50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }
            footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                text-align: center;
                color: #7f8c8d;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2</h1>
                <h2>Список лабораторных</h2>
            </header>
            
            <div class="menu">
                <a href="/lab1">Первая лабораторная</a>
                <a href="/lab2">Вторая лабораторная</a>
            </div>
            
            <a href="/" class="home-link">На главную</a>
            
            <footer>
                <p>Лелюх Роман Вячеславович, ФБИ-34, 3 курс, 2024</p>
            </footer>
        </div>
    </body>
    </html>""", 200, {"Content-Type": "text/html; charset=utf-8"}




@lab1.route('/lab1')
def lab():
    return """<!doctype html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Лабораторная 1</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
                color: #333;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 15px;
            }
            h2 {
                color: #3498db;
                margin-top: 30px;
                border-left: 4px solid #3498db;
                padding-left: 15px;
            }
            .content {
                font-size: 1.1em;
                text-align: justify;
                margin-bottom: 30px;
            }
            .routes-list {
                list-style: none;
                padding: 0;
                margin: 20px 0;
            }
            .routes-list li {
                margin: 10px 0;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 5px;
                border-left: 3px solid #3498db;
            }
            .routes-list a {
                color: #2c3e50;
                text-decoration: none;
                font-weight: bold;
            }
            .routes-list a:hover {
                color: #3498db;
                text-decoration: underline;
            }
            .back-link {
                display: inline-block;
                padding: 12px 25px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: all 0.3s ease;
                font-weight: bold;
                margin-top: 20px;
            }
            .back-link:hover {
                background: #2980b9;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .text-center {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Лабораторная работа 1</h1>
            
            <div class="content">
                <p>Flask — фреймворк для создания веб-приложений на языке
                программирования Python, использующий набор инструментов
                Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                называемых микрофреймворков — минималистичных каркасов
                веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
            </div>
            
            <h2>Список роутов</h2>
            <ul class="routes-list">
                <li><a href="/">Главная страница (/)</a></li>
                <li><a href="/index">Главная страница (/index)</a></li>
                <li><a href="/lab1/author">Автор (/lab1/author)</a></li>
                <li><a href="/lab1/image">Картинка (/lab1/image)</a></li>
                <li><a href="/lab1/counter">Счётчик (/lab1/counter)</a></li>
                <li><a href="/lab1/info">Редирект (/lab1/info)</a></li>
                <li><a href="/lab1/created">201 Created (/lab1/created)</a></li>
                <li><a href="/400">400 Bad Request</a></li>
                <li><a href="/401">401 Unauthorized</a></li>
                <li><a href="/402">402 Payment Required</a></li>
                <li><a href="/403">403 Forbidden</a></li>
                <li><a href="/405">405 Method Not Allowed</a></li>
                <li><a href="/418">418 I'm a teapot</a></li>
                <li><a href="/error500">500 Internal Server Error</a></li>
            </ul>
            
            <div class="text-center">
                <a href="/" class="back-link">Вернуться на главную</a>
            </div>
        </div>
    </body>
    </html>""", 200, {"Content-Type": "text/html; charset=utf-8"}

@lab1.route('/lab1/author')
def author():
    name = 'Лелюх Роман Вячеславович'
    group = 'ФБИ-34'
    faculty = 'ФБ'

    return """
    <!doctype html>
    <html>
        <body>
            <p>Студент: """ + name + """ </p>
            <p>Группа: """ + group + """ </p>
            <p>Факультет: """ + faculty + """ </p>
        </body>
    </html>
    """

@lab1.route('/lab1/image')
def image():
    image_path = url_for('static', filename='oak.jpg')
    css_path = url_for('static', filename='lab1.css')
    
    html_content = '''
    <!doctype html>
    <html>
        <head>
            <title>БМВ М8</title>
            <link rel="stylesheet" href="''' + css_path + '''">
        </head>
        <body class="image-page">
            <div class="container">
                <h1>МКА МКА</h1>
                <div class="image-wrlab1er">
                    <img src="''' + image_path + '''" alt="Дуб">
                </div>
                <p class="description">это м8</p>
            </div>
        </body>
    </html>
    '''
    
    headers = {
        "Content-Type": "text/html; charset=utf-8",
        "Content-Language": "ru-RU",
        "X-Custom-Header": "Flask-Image-Server",
        "X-Server-Version": "1.0.0",
        "X-Image-Name": "oak.jpg"
    }
    
    return html_content, 200, headers

count = 0

@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
    <!doctype html>
    <html>
        <body>
            Сколько раз вы сюда заходили ''' + str(count) + '''
            <hr>
            Дата и время: ''' + str(time) + ''' <br>
            Запрошенный адрес: ''' + url + ''' <br>
            Ваш IP-адрес: ''' + client_ip + ''' <br>
        </body>
    </html>
    '''

@lab1.route('/lab1/info')
def info():
    return redirect("/lab1/author")

@lab1.route('/lab1/created')
def created():
    return '''
    <!doctype html>
    <html>
        <body>
            <h1>Создайте успешно</h1>
            <div><i>что-то создано..</i>
        </body>
    </html>
    ''', 201


@lab1.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@lab1.route('/400')
def bad_request():
    return """<!doctype html>
    <html>
        <head>
            <title>400 Bad Request</title>
        </head>
        <body>
            <h1>400 Bad Request</h1>
            <p>Сервер не может обработать запрос из-за некорректного синтаксиса.</p>
            <a href="/">На главную</a>
        </body>
    </html>""", 400

@lab1.route('/401')
def unauthorized():
    return """<!doctype html>
    <html>
        <head>
            <title>401 Unauthorized</title>
        </head>
        <body>
            <h1>401 Unauthorized</h1>
            <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
            <a href="/">На главную</a>
        </body>
    </html>""", 401

@lab1.route('/402')
def payment_required():
    return """<!doctype html>
    <html>
        <head>
            <title>402 Payment Required</title>
        </head>
        <body>
            <h1>402 Payment Required</h1>
            <p>Запрос не может быть обработан до осуществления оплаты.</p>
            <a href="/">На главную</a>
        </body>
    </html>""", 402

@lab1.route('/403')
def forbidden():
    return """<!doctype html>
    <html>
        <head>
            <title>403 Forbidden</title>
        </head>
        <body>
            <h1>403 Forbidden</h1>
            <p>Доступ к запрашиваемому ресурсу запрещен.</p>
            <a href="/">На главную</a>
        </body>
    </html>""", 403

@lab1.route('/405')
def method_not_allowed():
    return """<!doctype html>
    <html>
        <head>
            <title>405 Method Not Allowed</title>
        </head>
        <body>
            <h1>405 Method Not Allowed</h1>
            <p>Метод, указанный в запросе, не разрешен для данного ресурса.</p>
            <a href="/">На главную</a>
        </body>
    </html>""", 405

@lab1.route('/418')
def teapot():
    return """<!doctype html>
    <html>
        <head>
            <title>418 I'm a teapot</title>
        </head>
        <body>
            <h1>418 I'm a teapot</h1>
            <p>Я чайник. Не могу заваривать кофе.</p>
            <a href="/">На главную</a>
        </body>
    </html>""", 418

@lab1.before_request
def log_request():
    """Логируем все запросы перед обработкой"""
    if request.path != '/favicon.ico':  # Игнорируем запросы favicon
        log_entry = {
            'ip': request.remote_addr,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'path': request.path,
            'method': request.method,
            'user_agent': request.headers.get('User-Agent', 'Unknown')[:50]
        }
        request_log.appendleft(log_entry)  # ← ИСПРАВЛЕНО




