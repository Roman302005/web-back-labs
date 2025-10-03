
from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from collections import deque

# Хранилище для лога запросов (ограничим последними 20 запросами)
request_log = deque(maxlen=20)

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



@app.route('/lab1')
def lab1():
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
        </body>
    </html>
    """

@app.route('/lab1/image')
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
                <div class="image-wrapper">
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
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    requested_path = request.path
    
    # Генерируем HTML для лога запросов
    log_html = ''
    for entry in request_log:
        log_html += f'''
        <tr>
            <td>{entry['timestamp']}</td>
            <td>{entry['ip']}</td>
            <td>{entry['method']}</td>
            <td>{entry['path']}</td>
            <td>{entry['user_agent']}</td>
        </tr>'''
    
    return f"""<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Страница не найдена</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        }}
        .error-header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .error-code {{
            font-size: 6em;
            font-weight: bold;
            color: #e74c3c;
            margin: 0;
            text-shadow: 3px 3px 0 #f8f9fa;
        }}
        .error-title {{
            font-size: 2em;
            color: #2c3e50;
            margin: 10px 0;
        }}
        .error-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        .error-info h3 {{
            color: #3498db;
            margin-top: 0;
        }}
        .error-info p {{
            margin: 5px 0;
        }}
        .log-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        .log-table th,
        .log-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .log-table th {{
            background: #3498db;
            color: white;
            font-weight: bold;
        }}
        .log-table tr:hover {{
            background: #f5f5f5;
        }}
        .home-link {{
            display: inline-block;
            padding: 15px 30px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s ease;
            margin-top: 20px;
        }}
        .home-link:hover {{
            background: #2980b9;
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }}
        .text-center {{
            text-align: center;
        }}
        .teapot {{
            font-size: 4em;
            margin: 20px 0;
            animation: bounce 2s infinite;
        }}
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{transform: translateY(0);}}
            40% {{transform: translateY(-20px);}}
            60% {{transform: translateY(-10px);}}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error-header">
            <div class="teapot">🧭</div>
            <h1 class="error-code">404</h1>
            <h2 class="error-title">Ой! Заблудились?</h2>
        </div>

        <div class="error-info">
            <h3>Информация о запросе:</h3>
            <p><strong>Ваш IP-адрес:</strong> {client_ip}</p>
            <p><strong>Дата и время:</strong> {access_date}</p>
            <p><strong>Запрошенный адрес:</strong> {requested_path}</p>
            <p><strong>User-Agent:</strong> {request.headers.get('User-Agent', 'Unknown')[:80]}...</p>
        </div>

        <div class="error-info">
            <h3>Журнал последних запросов:</h3>
            <table class="log-table">
                <thead>
                    <tr>
                        <th>Время</th>
                        <th>IP-адрес</th>
                        <th>Метод</th>
                        <th>Путь</th>
                        <th>User-Agent</th>
                    </tr>
                </thead>
                <tbody>
                    {log_html if log_html else '''
                    <tr>
                        <td colspan="5" style="text-align: center; color: #7f8c8d;">
                            Пока нет записей в журнале
                        </td>
                    </tr>'''}
                </tbody>
            </table>
        </div>

        <div class="text-center">
            <a href="/" class="home-link">Вернуться на главную</a>
        </div>
    </div>
</body>
</html>""", 404


@app.route('/400')
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

@app.route('/401')
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

@app.route('/402')
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

@app.route('/403')
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

@app.route('/405')
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

@app.route('/418')
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


@app.route('/error500')
def error500():
    # Вызываем ошибку деления на ноль
    result = 1 / 0
    return "Этот код никогда не выполнится"

@app.errorhandler(500)
def internal_server_error(err):
    return """<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>500 - Внутренняя ошибка сервера</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
            max-width: 500px;
        }
        .error-code {
            font-size: 6em;
            font-weight: bold;
            color: #c23616;
            margin: 0;
            text-shadow: 3px 3px 0 #f8f9fa;
        }
        .error-title {
            font-size: 2em;
            color: #2c3e50;
            margin: 10px 0;
        }
        .error-message {
            font-size: 1.2em;
            color: #7f8c8d;
            margin: 20px 0;
            line-height: 1.6;
        }
        .error-icon {
            font-size: 4em;
            margin: 20px 0;
            animation: shake 0.5s infinite;
        }
        .home-link {
            display: inline-block;
            margin-top: 20px;
            padding: 15px 30px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .home-link:hover {
            background: #2980b9;
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        @keyframes shake {
            0%, 100% {transform: translateX(0);}
            25% {transform: translateX(-5px);}
            75% {transform: translateX(5px);}
        }
        .tech-info {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #e74c3c;
            text-align: left;
        }
        .tech-info h3 {
            color: #e74c3c;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="error-icon">⚡</div>
        <h1 class="error-code">500</h1>
        <h2 class="error-title">Внутренняя ошибка сервера</h2>
        <p class="error-message">
            Что-то пошло не так на нашей стороне. Наши инженеры уже бегут 
            с огнетушителями и отвёртками устранять проблему!
        </p>
        <p class="error-message">
            Пожалуйста, попробуйте обновить страницу через несколько минут.
        </p>
        
        <div class="tech-info">
            <h3>Техническая информация:</h3>
            <p>Произошла непредвиденная ошибка при обработке вашего запроса.</p>
            <p>Рекомендуется запустить сервер с флагом --debug для подробной информации об ошибке.</p>
        </div>
        
        <a href="/" class="home-link">Вернуться на главную</a>
    </div>
</body>
</html>""", 500



@app.before_request
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
        request_log.appendleft(log_entry)

@app.route('/laba2/a')
def a1():
    return 'без слэша'

@app.route('/laba2/a/')
def a12():
    return 'со слэшем'    




flower_list = ['роза', 'тюльпан', 'ромашка', 'лилия']

@app.route('/laba2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404) 
    else:
        return 'цветок: ' + flower_list[flower_id]


@app.route('/laba2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов:{len(flower_list)} </p>
    <p>Полный список:{flower_list} </p>
    </body>
</html>
'''

@app.route('/lab2/example')
def examplee():
    name = 'Лелюх Роман'
    return render_template('example.html', name=name)
