from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response
import datetime
from collections import deque

request_log = deque(maxlen=20)

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def labbbb():
    name = request.cookies.get('name', 'Аноним')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age', 'не указан')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)



@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del/cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age = age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    
    if color or bg_color or font_size:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    
    return render_template('lab3/settings.html', 
                         color=color or '#000000',
                         bg_color=bg_color or '#ffffff', 
                         font_size=font_size or '16')

@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    if not fio: errors['fio'] = "Заполните ФИО"
    if not shelf: errors['shelf'] = "Выберите полку"
    if not age: errors['age'] = "Укажите возраст"
    elif not age.isdigit() or not (1 <= int(age) <= 120):
        errors['age'] = "Возраст от 1 до 120 лет"
    if not departure: errors['departure'] = "Укажите пункт выезда"
    if not destination: errors['destination'] = "Укажите пункт назначения"
    if not date: errors['date'] = "Укажите дату"
    
    if errors:
        return render_template('lab3/ticket_form.html', errors=errors, 
                             fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                             age=age, departure=departure, destination=destination,
                             date=date, insurance=insurance)
    
    price = 1000 if int(age) >= 18 else 700
    if shelf in ['lower', 'lower-side']: price += 100
    if linen == 'on': price += 75
    if baggage == 'on': price += 250
    if insurance == 'on': price += 150
    
    ticket_type = "Детский билет" if int(age) < 18 else "Взрослый билет"
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, price=price, ticket_type=ticket_type)

@lab3.route('/lab3/ticket-form')
def ticket_form():
    return render_template('lab3/ticket_form.html')



@lab3.route('/lab3/clear-settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color') 
    resp.delete_cookie('font_size')
    return resp