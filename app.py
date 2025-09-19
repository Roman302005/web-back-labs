from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/web')
def web():
    return """<!doctype html>
    <html>
        <head>
            <title>Web Server</title>
        </head>
        <body>
            <h1>web-сервер на flask</h1>
            <a href="/author">author</a><br>
            <a href="/image">Картинка</a><br>
            <a href="/counter">Cчётчик</a><br>
            <a href="/info">Редирект</a><br>
            <a href="/lab1/created">201</a>
        </body>
    </html>""", 200, {"X-Server": "sample",
                     "Content-Type": "text/html; charset=utf-8" 
                     }

@app.route('/author')
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
            <a href="/web">web</a>
        </body>
    </html>
    """

@app.route('/image')
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
                <a href="/web" class="back-link">← Вернуться на главную</a>
            </div>
        </body>
    </html>
    '''

count = 0

@app.route('/counter')
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

@app.route('/info')
def info():
    return redirect("/author")

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

@app.errorhandler(404)
def not_found(err):
    return 'такой страницы нет', 404