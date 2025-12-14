from flask import Blueprint, render_template, request, session
import json

lab6 = Blueprint('lab6', __name__)

# Список офисов с разной стоимостью аренды
offices = []
for i in range(1, 11):
    offices.append({
        'number': i,
        'tenant': '',
        'price': 900 + i % 3  # Стоимость: 900, 901, 902, 900, 901, 902 и т.д.
    })

@lab6.route('/lab6/')
def main():
    login = session.get('login')
    
    # Вычисляем общую стоимость арендованных пользователем офисов
    total_cost = 0
    if login:
        for office in offices:
            if office['tenant'] == login:
                total_cost += office['price']
    
    return render_template('lab6/lab6.html', login=login, total_cost=total_cost)

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    method = data.get('method')
    params = data.get('params')
    id = data.get('id')
    
    if method == 'info':
        # Возвращаем информацию о всех офисах
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    elif method == 'booking':
        # Проверка авторизации
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }
        
        office_number = params
        # Бронирование офиса
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
        
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': id
        }
    
    elif method == 'cancellation':
        # Проверка авторизации
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }
        
        office_number = params
        # Снятие аренды офиса
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 5,
                            'message': 'Office is not booked'
                        },
                        'id': id
                    }
                elif office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Not your booking'
                        },
                        'id': id
                    }
                else:
                    # Снимаем аренду
                    office['tenant'] = ''
                    return {
                        'jsonrpc': '2.0',
                        'result': 'success',
                        'id': id
                    }
        
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': id
        }
    
    else:
        # Метод не найден
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': id
        }