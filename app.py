from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

@app.route('/lab1')
@app.route('/lab1/web')
def web():
    return """<!doctype html>
    <html>
        <head>
            <title>Web Server</title>
        </head>
        <body>
            <h1>web-сервер на flask</h1>
            <a href="/index">index</a><br>
            <a href="/lab1/author">author</a><br>
            <a href="/lab1/image">Картинка</a><br>
            <a href="/lab1/counter">Cчётчик</a><br>
            <a href="/lab1/info">Редирект</a><br>
            <a href="/lab1/created">201</a>
            <a href="/lab1/counter/clear">Очистка</a>
        </body>
    </html>""", 200, {"X-Server": "sample",
                     "Content-Type": "text/html; charset=utf-8" 
                     }



from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/index')
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
            </div>
            
            <footer>
                <p>Лелюх Роман Вячеславович, ФБИ-34, 3 курс, 2024</p>
            </footer>
        </div>
    </body>
    </html>""", 200, {"Content-Type": "text/html; charset=utf-8"}



@app.route('/lab1/author')
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
            <a href="/lab1/web">web</a>
        </body>
    </html>
    """

@app.route('/lab1/image')
def image():
    image_path = url_for('static', filename='oak.jpg')
    css_path = url_for('static', filename='lab1.css')
    
    return '''
    <!doctype html>
    <html>
        <head>
            <title>БМВ М8</title>
            <link rel="stylesheet" href="''' + css_path + '''">
        </head>
        <body class="image-page">
            <div class="container">
                <h1>МКА МКА</h1>
                <div class="image-wrapper">
                    <img src="''' + image_path + '''" alt="Дуб">
                </div>
                <p class="description">это м8</p>
                <a href="/lab1/web" class="back-link">← Вернуться на главную</a>
            </div>
        </body>
    </html>
    '''

count = 0

@app.route('/lab1/counter')
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

@app.route('/lab1/info')
def info():
    return redirect("/lab1/author")

@app.route('/lab1/created')
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


@app.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@app.errorhandler(404)
def not_found(err):
    return 'такой страницы нет', 404


