from flask import Blueprint, render_template, request, redirect, session
import datetime
from collections import deque
from flask import request

request_log = deque(maxlen=20)

lab4 = Blueprint('lab4', __name__)
tree_count = 0

@lab4.route('/lab4/')
def labs():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
  
    x1 = int(x1)
    x2 = int(x2)
    
 
    if x2 == 0:
        return render_template('lab4/div.html', error='Делитель не может быть равен нулю!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    x1 = float(x1) if x1 else 0
    x2 = float(x2) if x2 else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/multiply-form')
def multiply_form():
    return render_template('lab4/multiply-form.html')

@lab4.route('/lab4/multiply', methods=['POST'])
def multiply():
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')
    
    x1 = float(x1) if x1 else 1
    x2 = float(x2) if x2 else 1
    
    result = x1 * x2
    return render_template('lab4/multiply.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/subtract-form')
def subtract_form():
    return render_template('lab4/subtract-form.html')

@lab4.route('/lab4/subtract', methods=['POST'])
def subtract():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/subtract.html', error='Оба поля должны быть заполнены!')
    
    x1 = float(x1)
    x2 = float(x2)
    
    result = x1 - x2
    return render_template('lab4/subtract.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/power-form')
def power_form():
    return render_template('lab4/power-form.html')

@lab4.route('/lab4/power', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/power.html', error='Оба поля должны быть заполнены!')
    
    x1 = float(x1)
    x2 = float(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/power.html', error='Оба числа не могут быть равны нулю!')
    
    result = x1 ** x2
    return render_template('lab4/power.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'POST':
        operation = request.form.get('operation')
        
        if operation == 'cut' and tree_count > 0:
            tree_count -= 1
        elif operation == 'plant' and tree_count < 10:
            tree_count += 1
        
        return redirect('/lab4/tree')
    
    return render_template('lab4/tree.html', tree_count=tree_count)

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр', 'gender': 'мужской'},
    {'login': 'bob', 'password': '555', 'name': 'Роберт', 'gender': 'мужской'},
    {'login': 'cat', 'password': '777', 'name': 'Екатерина', 'gender': 'женский'},
    {'login': 'dog', 'password': '999', 'name': 'Дарья', 'gender': 'женский'},
    {'login': 'admin', 'password': 'admin', 'name': 'Администратор', 'gender': 'мужской'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user_name = ''
            for user in users:
                if user['login'] == login:
                    user_name = user['name']
                    break
            return render_template('lab4/login.html', authorized=authorized, login=login, user_name=user_name)
        else:
            return render_template('lab4/login.html', authorized=False, login='')
    
    login_input = request.form.get('login')
    password = request.form.get('password')
    
    if not login_input:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login_input)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login_input)
    
    for user in users:
        if login_input == user['login'] and password == user['password']:
            session['login'] = login_input
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login_input)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'POST':
        temperature = request.form.get('temperature')
        
        if not temperature:
            return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
        
        try:
            temp = float(temperature)
        except ValueError:
            return render_template('lab4/fridge.html', error='Ошибка: введите числовое значение')
        
        if temp < -12:
            return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
        elif temp > -1:
            return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
        elif -12 <= temp <= -9:
            snowflakes = '❄️❄️❄️'
            return render_template('lab4/fridge.html', temperature=temp, snowflakes=snowflakes)
        elif -8 <= temp <= -5:
            snowflakes = '❄️❄️'
            return render_template('lab4/fridge.html', temperature=temp, snowflakes=snowflakes)
        elif -4 <= temp <= -1:
            snowflakes = '❄️'
            return render_template('lab4/fridge.html', temperature=temp, snowflakes=snowflakes)
    
    return render_template('lab4/fridge.html')


@lab4.route('/lab4/seed', methods=['GET', 'POST'])
def seed():
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')

        prices = {
            'barley': 12000,  
            'oats': 8500,     
            'wheat': 9000,    
            'rye': 15000      
        }
        
        grain_names = {
            'barley': 'ячмень',
            'oats': 'овёс', 
            'wheat': 'пшеница',
            'rye': 'рожь'
        }
        
        if not weight:
            return render_template('lab4/seed.html', error='Ошибка: не указан вес')
        
        try:
            weight_float = float(weight)
        except ValueError:
            return render_template('lab4/seed.html', error='Ошибка: введите числовое значение веса')
        
        if weight_float <= 0:
            return render_template('lab4/seed.html', error='Ошибка: вес должен быть больше 0')
        
        if weight_float > 100:
            return render_template('lab4/seed.html', error='Извините, такого объёма сейчас нет в наличии')
        
        price_per_ton = prices.get(grain_type)
        if not price_per_ton:
            return render_template('lab4/seed.html', error='Ошибка: выберите тип зерна')
        
        total = weight_float * price_per_ton
        
        discount = 0
        if weight_float > 10:
            discount = total * 0.1
            total -= discount
        
        grain_name = grain_names.get(grain_type)
        
        return render_template('lab4/seed.html', 
                             success=True,
                             grain=grain_name,
                             weight=weight_float,
                             total=total,
                             discount=discount)
    
    return render_template('lab4/seed.html')