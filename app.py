from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
import os
from collections import deque
from lab1.lab1 import lab1
from lab2.lab2 import lab2
from lab3.lab3 import lab3
from lab4.lab4 import lab4
from lab5.lab5 import lab5
from lab6.lab6 import lab6
from lab7.lab7 import lab7 

from rgz.rgz import rgz
request_log = deque(maxlen=20)
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(rgz)

app.secret_key = 'секретно-секретный секрет'

@app.route('/')
def main():
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
            .lab-section {
                margin: 30px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 4px solid #3498db;
            }
            .lab-section h3 {
                color: #2c3e50;
                margin-top: 0;
            }
            .lab-links {
                list-style: none;
                padding: 0;
            }
            .lab-links li {
                margin: 8px 0;
                padding: 8px 12px;
                background: white;
                border-radius: 5px;
                border-left: 3px solid #e74c3c;
            }
            .lab-links a {
                color: #2c3e50;
                text-decoration: none;
                font-weight: bold;
            }
            .lab-links a:hover {
                color: #3498db;
                text-decoration: underline;
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
                <a href="/lab1">Лабораторная работа 1</a>
                <a href="/lab2">Лабораторная работа 2</a>
               <a href="/lab3/">Лабораторная работа 3</a>
               <a href="/lab4/">Лабораторная работа 4</a>
               <a href="/lab5">Лабораторная работа 5</a>
               <a href="/lab6">Лабораторная работа 6</a>
               <a href="/lab7">Лабораторная работа 7</a>
               <a href="/rgz">RGZ Мессенджер</a>
            </div>

            <div class="lab-section">
                <h3>🔧 Лабораторная работа 1 - Основы Flask</h3>
                <ul class="lab-links">
                    <li><a href="/lab1/author">👨‍🎓 Автор</a></li>
                    <li><a href="/lab1/image">🖼️ Картинка</a></li>
                    <li><a href="/lab1/counter">🔢 Счётчик посещений</a></li>
                    <li><a href="/lab1/counter/clear">🔄 Сброс счётчика</a></li>
                    <li><a href="/lab1/info">↪️ Редирект</a></li>
                    <li><a href="/lab1/created">✅ 201 Created</a></li>
                </ul>
            </div>

            <div class="lab-section">
                <h3>⚡ Лабораторная работа 2 - Расширенные возможности</h3>
                <ul class="lab-links">
                    <li><a href="/lab2/flowers">🌷 Работа с цветами</a></li>
                    <li><a href="/lab2/flowers/0">🌹 Пример цветка</a></li>
                    <li><a href="/lab2/add_flower/орхидея">➕ Добавить цветок</a></li>
                    <li><a href="/lab2/clear_flowers">🗑️ Очистить цветы</a></li>
                    <li><a href="/lab2/calc">🧮 Калькулятор</a></li>
                    <li><a href="/lab2/calc/5/3">🔢 Пример вычислений</a></li>
                    <li><a href="/lab2/books">📚 Список книг</a></li>
                    <li><a href="/lab2/cars">🚗 Галерея автомобилей</a></li>
                    <li><a href="/lab2/example">🎨 Пример шаблона</a></li>
                    <li><a href="/lab2/filters">🔧 Фильтры Jinja2</a></li>
                    <li><a href="/laba2/a">🔗 Без слэша</a></li>
                    <li><a href="/laba2/a/">🔗 Со слэшем</a></li>
                </ul>
            </div>

            <div class="lab-section">
                <h3>🚨 Коды ошибок HTTP</h3>
                <ul class="lab-links">
                    <li><a href="/400">❌ 400 Bad Request</a></li>
                    <li><a href="/401">🔐 401 Unauthorized</a></li>
                    <li><a href="/402">💳 402 Payment Required</a></li>
                    <li><a href="/403">🚫 403 Forbidden</a></li>
                    <li><a href="/405">⚡ 405 Method Not Allowed</a></li>
                    <li><a href="/418">🍵 418 I'm a teapot</a></li>
                    <li><a href="/error500">💥 500 Internal Server Error</a></li>
                </ul>
            </div>
            
            <footer>
                <p>Лелюх Роман Вячеславович, ФБИ-34, 3 курс, 2025</p>
            </footer>
        </div>
    </body>
    </html>""", 200, {"Content-Type": "text/html; charset=utf-8"}




@app.errorhandler(500)
def internal_server_error(err=None):  
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

@app.errorhandler(404)
def not_found(err=None):  # Также добавляем значение по умолчанию для consistency
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    requested_path = request.path
    
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

if __name__ == '__main__':
    app.run(debug=True)