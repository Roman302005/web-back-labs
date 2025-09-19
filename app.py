from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/web')
def web():
    return """<!doctype html>
    <html>
        <body>
            <h1>web-сервер на flask</h1>
            <a href="/author">author</a>
            <a href="/image">Картинка</a>
            <a href="/counter">Cчётчик</a>
            <a href="/info">Редирект</a>
            <a href="/lab1/created">201</a>
        </body>
    </html>"""


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
    path = url_for('static', filename='oak.jpg')
    return '''
    <!doctype html>
    <html>
        <body>
            <h1>М8</h1>
            <img src=" ''' + path + ''' ">
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