from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response
import datetime
from collections import deque
from flask import request

request_log = deque(maxlen=20)

lab4 = Blueprint('lab4', __name__)


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
    
    # Валидация: проверка на пустые поля
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    # Преобразование в числа
    x1 = int(x1)
    x2 = int(x2)
    
    # Проверка деления на ноль
    if x2 == 0:
        return render_template('lab4/div.html', error='Делитель не может быть равен нулю!')
    
    # Вычисление результата
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)