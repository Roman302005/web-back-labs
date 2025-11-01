from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response
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