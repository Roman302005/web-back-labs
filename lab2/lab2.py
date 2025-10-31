from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
from collections import deque

request_log = deque(maxlen=20)

lab2= Blueprint('lab2', __name__)



flower_list = ['роза', 'тюльпан', 'ромашка', 'лилия']

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Вишнёвый сад', 'genre': 'Пьеса', 'pages': 96},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 128},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 576}
]

cars = [
    {'name': 'BMW M8', 'image': '1.jpg', 'description': 'Спортивный автомобиль немецкого производства с мощным двигателем'},
    {'name': 'Mercedes S-Class', 'image': '2.jpg', 'description': 'Представительский седан с роскошным интерьером'},
    {'name': 'Audi R8', 'image': '3.jpg', 'description': 'Спортивный автомобиль с полным приводом и стильным дизайном'},
    {'name': 'Porsche 911', 'image': '4.jpg', 'description': 'Легендарный спортивный автомобиль с задним расположением двигателя'},
    {'name': 'Tesla Model S', 'image': '5.jpg', 'description': 'Электрический седан с автопилотом и высокой производительностью'},
    {'name': 'Lamborghini Aventador', 'image': '6.jpg', 'description': 'Суперкар с агрессивным дизайном и мощным V12 двигателем'},
    {'name': 'Ferrari F8', 'image': '7.jpg', 'description': 'Итальянский суперкар с выдающимися динамическими характеристиками'},
    {'name': 'Ford Mustang', 'image': '8.jpg', 'description': 'Американский маслкар с культовым дизайном'},
    {'name': 'Chevrolet Camaro', 'image': '9.jpg', 'description': 'Спортивный автомобиль с мускулистым внешним видом'},
    {'name': 'Nissan GT-R', 'image': '10.jpg', 'description': 'Японский суперкар с технологичным оснащением'},
    {'name': 'Toyota Supra', 'image': '11.jpg', 'description': 'Спортивное купе с богатой историей'},
    {'name': 'Honda Civic Type R', 'image': '12.jpg', 'description': 'Горячая версия хэтчбека с передним приводом'},
    {'name': 'Subaru WRX STI', 'image': '13.jpg', 'description': 'Полноприводный спортивный седан для любителей ралли'},
    {'name': 'Mazda MX-5', 'image': '14.jpg', 'description': 'Компактный родстер с задним приводом'},
    {'name': 'Volkswagen Golf GTI', 'image': '15.jpg', 'description': 'Культовый хот-хэтч с отличной управляемостью'},
    {'name': 'Hyundai Veloster N', 'image': '12.jpg', 'description': 'Спортивный хэтчбек с асимметричными дверями'},
    {'name': 'Kia Stinger', 'image': '13.jpg', 'description': 'Спортивный лифтбек с задним приводом'},
    {'name': 'Lexus LC 500', 'image': '11.jpg', 'description': 'Роскошное купе с атмосферным V8'},
    {'name': 'Jaguar F-Type', 'image': '9.jpg', 'description': 'Британское спортивное купе с элегантным дизайном'},
    {'name': 'Aston Martin DB11', 'image': '1.jpg', 'description': 'Гранд турер с роскошным интерьером'}
]


@lab2.route('/lab2')
def lab():
    favicon_url = url_for('static', filename='favicon.ico')
    return f"""<!doctype html>
    <html lang="ru">
    <head>
        <link rel="icon" type="image/x-icon" href="{favicon_url}">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Лабораторная 2</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 15px;
            }}
            h2 {{
                color: #3498db;
                margin-top: 30px;
                border-left: 4px solid #3498db;
                padding-left: 15px;
            }}
            .routes-list {{
                list-style: none;
                padding: 0;
                margin: 20px 0;
            }}
            .routes-list li {{
                margin: 10px 0;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 5px;
                border-left: 3px solid #3498db;
            }}
            .routes-list a {{
                color: #2c3e50;
                text-decoration: none;
                font-weight: bold;
            }}
            .routes-list a:hover {{
                color: #3498db;
                text-decoration: underline;
            }}
            .back-link {{
                display: inline-block;
                padding: 12px 25px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: all 0.3s ease;
                font-weight: bold;
                margin-top: 20px;
            }}
            .back-link:hover {{
                background: #2980b9;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            .home-link {{
                display: inline-block;
                padding: 10px 20px;
                background: #2c3e50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 10px 5px;
            }}
            .text-center {{
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Лабораторная работа 2</h1>
            
            <h2>Работа с цветами</h2>
            <ul class="routes-list">
                <li><a href="/lab2/flowers">Все цветы</a> - просмотр всех цветов и их количества</li>
                <li><a href="/lab2/flowers/0">Пример цветка (ID: 0)</a></li>
                <li><a href="/lab2/add_flower/орхидея">Добавить цветок "орхидея"</a></li>
                <li><a href="/lab2/clear_flowers">Очистить список цветов</a></li>
            </ul>

            <h2>Математические операции</h2>
            <ul class="routes-list">
                <li><a href="/lab2/calc">Калькулятор (по умолчанию 1/1)</a></li>
                <li><a href="/lab2/calc/5/3">Пример: 5 и 3</a></li>
                <li><a href="/lab2/calc/10/2">Пример: 10 и 2</a></li>
                <li><a href="/lab2/calc/8">Пример: 8 и 1</a></li>
            </ul>

            <h2>Книги</h2>
            <ul class="routes-list">
                <li><a href="/lab2/books">Список книг</a> - просмотр списка книг с авторами и жанрами</li>
            </ul>

            <h2>Автомобили</h2>
            <ul class="routes-list">
                <li><a href="/lab2/cars">Галерея автомобилей</a> - просмотр автомобилей с изображениями</li>
            </ul>

            <h2>Шаблоны</h2>
            <ul class="routes-list">
                <li><a href="/lab2/example">Пример шаблона</a> - демонстрация работы с шаблонами</li>
                <li><a href="/lab2/filters">Фильтры Jinja2</a> - демонстрация фильтров в шаблонах</li>
            </ul>
            
            <div class="text-center">
                <a href="/" class="back-link">Вернуться на главную</a>
                <a href="/" class="home-link">На главную</a>
            </div>
        </div>
    </body>
    </html>""", 200, {"Content-Type": "text/html; charset=utf-8"}

@lab2.route('/lab2/books')
def books_list():
    """Страница со списком книг"""
    return render_template('books.html', books=books)

@lab2.route('/lab2/cars')
def cars_gallery():
    """Страница с галереей автомобилей"""
    return render_template('cars.html', cars=cars)


@lab2.route('/laba2/a')
def a1():
    return 'без слэша'


@lab2.route('/laba2/a/')
def a12():
    return 'со слэшем'    


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404) 
    else:
        flower_name = flower_list[flower_id]
        return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Цветок #{flower_id}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }}
        .flower-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        .flower-name {{
            font-size: 1.5em;
            color: #e74c3c;
            font-weight: bold;
        }}
        .links {{
            margin-top: 30px;
            text-align: center;
        }}
        .links a {{
            display: inline-block;
            padding: 12px 24px;
            margin: 8px 12px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s ease;
            font-weight: bold;
        }}
        .links a:hover {{
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Информация о цветке</h1>
        
        <div class="flower-info">
            <p><strong>ID цветка:</strong> {flower_id}</p>
            <p><strong>Название:</strong> <span class="flower-name">{flower_name}</span></p>
            <p><strong>Всего цветов в базе:</strong> {len(flower_list)}</p>
        </div>
        
        <div class="links">
            <a href="/lab2/flowers">Посмотреть все цветы</a>
            <a href="/lab2">Вернуться к лабораторной работе 2</a>
            <a href="/">На главную</a>
        </div>
    </div>
</body>
</html>
'''
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)  # ← ИСПРАВЛЕНО
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

@lab2.route('/lab2/add_flower/')
def add_flower_without_name():
    return 'вы не задали имя цветка', 400

@lab2.route('/lab2/flowers')
def all_flowers():
    flowers_html = ''
    for i, flower in enumerate(flower_list):
        flowers_html += f'<li><a href="/lab2/flowers/{i}">{flower}</a></li>'
    
    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Все цветы</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }}
        .stats {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        .flower-list {{
            list-style: none;
            padding: 0;
        }}
        .flower-list li {{
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 3px solid #e74c3c;
        }}
        .flower-list a {{
            color: #2c3e50;
            text-decoration: none;
            font-weight: bold;
        }}
        .flower-list a:hover {{
            color: #3498db;
            text-decoration: underline;
        }}
        .links {{
            margin-top: 30px;
            text-align: center;
        }}
        .links a {{
            display: inline-block;
            padding: 12px 24px;
            margin: 8px 12px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s ease;
            font-weight: bold;
        }}
        .links a:hover {{
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .clear-link {{
            background: #e74c3c !important;
        }}
        .clear-link:hover {{
            background: #c23616 !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Все цветы</h1>
        
        <div class="stats">
            <p><strong>Общее количество цветов:</strong> {len(flower_list)}</p>
        </div>
        
        <h2>Список цветов:</h2>
        <ul class="flower-list">
            {flowers_html if flowers_html else '<li>Список цветов пуст</li>'}
        </ul>
        
        <div class="links">
            <a href="/lab2">Вернуться к лабораторной работе 2</a>
            <a href="/lab2/clear_flowers" class="clear-link">Очистить список цветов</a>
            <a href="/">На главную</a>
        </div>
    </div>
</body>
</html>
'''

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list.clear()
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Список цветов очищен</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #28a745;
        }
        .links {
            margin-top: 30px;
            text-align: center;
        }
        .links a {
            display: inline-block;
            padding: 12px 24px;
            margin: 8px 12px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        .links a:hover {
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Список цветов очищен</h1>
        
        <div class="success-message">
            <p><strong>Все цветы успешно удалены из списка!</strong></p>
            <p>Список цветов теперь пуст.</p>
        </div>
        
        <div class="links">
            <a href="/lab2/flowers">Посмотреть все цветы</a>
            <a href="/lab2">Вернуться к лабораторной работе 2</a>
            <a href="/">На главную</a>
        </div>
    </div>
</body>
</html>
'''

@lab2.route('/lab2/calc')
def calc_default():
    """Пересылает на /lab2/calc/1/1"""
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    """Пересылает на /lab2/calc/a/1"""
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    """Выполняет математические операции с двумя числами"""
    try:
        sum_result = a + b
        diff_result = a - b
        mult_result = a * b
        
        if b != 0:
            div_result = a / b
            div_display = f"{div_result:.2f}"
        else:
            div_result = "Ошибка: деление на ноль"
            div_display = div_result
            
        pow_result = a ** b
        
    except Exception as e:
        return f"Ошибка при вычислениях: {e}", 500
    
    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }}
        .numbers {{
            background: #3498db;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .numbers h2 {{
            margin: 0;
            font-size: 2em;
        }}
        .operations {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }}
        .operation-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
            text-align: center;
        }}
        .operation-name {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .operation-result {{
            font-size: 1.2em;
            color: #e74c3c;
            font-weight: bold;
        }}
        .links {{
            margin-top: 30px;
            text-align: center;
        }}
        .links a {{
            display: inline-block;
            padding: 12px 24px;
            margin: 8px 12px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s ease;
            font-weight: bold;
        }}
        .links a:hover {{
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Математические операции</h1>
        
        <div class="numbers">
            <h2>{a} и {b}</h2>
        </div>
        
        <div class="operations">
            <div class="operation-card">
                <div class="operation-name">Сумма</div>
                <div class="operation-result">{a} + {b} = {sum_result}</div>
            </div>
            <div class="operation-card">
                <div class="operation-name">Разность</div>
                <div class="operation-result">{a} - {b} = {diff_result}</div>
            </div>
            <div class="operation-card">
                <div class="operation-name">Умножение</div>
                <div class="operation-result">{a} × {b} = {mult_result}</div>
            </div>
            <div class="operation-card">
                <div class="operation-name">Деление</div>
                <div class="operation-result">{a} ÷ {b} = {div_display}</div>
            </div>
            <div class="operation-card">
                <div class="operation-name">Степень</div>
                <div class="operation-result">{a}<sup>{b}</sup> = {pow_result}</div>
            </div>
        </div>
        
        <div class="links">
            <a href="/lab2/calc/5/3">Пример: 5 и 3</a>
            <a href="/lab2/calc/10/2">Пример: 10 и 2</a>
            <a href="/lab2">Вернуться к лабораторной работе 2</a>
            <a href="/">На главную</a>
        </div>
    </div>
</body>
</html>
'''

@lab2.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Лелюх Роман', 2, '34', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                         name=name, lab_num=lab_num, group=group,
                         course=course, fruits=fruits)

@lab2.route('/lab2/filters')
def filters():
    phrase = "<b>0 сколько нам открытий чудных...</b>"
    return render_template('filter.html', phrase=phrase)

