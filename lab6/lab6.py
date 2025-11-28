from flask import Blueprint, render_template, request, session, jsonify
import json

lab6 = Blueprint('lab6', __name__)

# Список офисов
offices = []
for i in range(1, 11):
    offices.append({
        'number': i,
        'tenant': ''
    })

@lab6.route('/lab6/')
def main():
    login = session.get('login')
    return render_template('lab6/lab6.html', login=login)

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def json_rpc_api():
    data = request.get_json()
    
    if not data:
        return json.dumps({
            'jsonrpc': '2.0',
            'error': {
                'code': -32700,
                'message': 'Parse error'
            },
            'id': None
        })
    
    method = data.get('method')
    params = data.get('params')
    id = data.get('id')
    
    if method == 'info':
        return json.dumps({
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        })
    
    elif method == 'booking':
        # Проверка авторизации через вашу существующую систему
        if 'login' not in session or not session['login']:
            return json.dumps({
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            })
        
        office_number = params
        login = session['login']
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return json.dumps({
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    })
                
                office['tenant'] = login
                return json.dumps({
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                })
        
        return json.dumps({
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': id
        })
    
    elif method == 'cancellation':
        # Проверка авторизации через вашу существующую систему
        if 'login' not in session or not session['login']:
            return json.dumps({
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            })
        
        office_number = params
        login = session['login']
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == login:
                    office['tenant'] = ''
                    return json.dumps({
                        'jsonrpc': '2.0',
                        'result': 'success',
                        'id': id
                    })
                elif office['tenant'] != '':
                    return json.dumps({
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Not your booking'
                        },
                        'id': id
                    })
        
        return json.dumps({
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': id
        })
    
    else:
        return json.dumps({
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': id
        })