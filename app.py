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
            .content {
                font-size: 1.1em;
                text-align: justify;
                margin-bottom: 30px;
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
    return """<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Страница не найдена</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            max-width: 500px;
        }
        .error-code {
            font-size: 6em;
            font-weight: bold;
            color: #e74c3c;
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
        .teapot {
            font-size: 4em;
            margin: 20px 0;
            animation: bounce 2s infinite;
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
            border: none;
            cursor: pointer;
        }
        .home-link:hover {
            background: #2980b9;
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
            40% {transform: translateY(-20px);}
            60% {transform: translateY(-10px);}
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="teapot">🧭</div>
        <h1 class="error-code">404</h1>
        <h2 class="error-title">Ой! Заблудились?</h2>
        <p class="error-message">
            Кажется, вы свернули не туда. Эта страница отправилась в космическое 
            путешествие и пока не вернулась. Возможно, она просто затерялась 
            среди звёзд и галактик...
        </p>
        <p class="error-message">
            Не волнуйтесь! Наш навигационный компас поможет вам вернуться 
            на безопасную орбиту.
        </p>
        <a href="/" class="home-link">Вернуться на главную</a>
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