from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
import random

lab9 = Blueprint('lab9', __name__)

# Новогодние подарки и поздравления
GIFTS = [
    {"id": 1, "image": "🎁", "congratulation": "С Новым Годом! Желаю счастья и удачи!", "gift": "🎄"},
    {"id": 2, "image": "🎁", "congratulation": "Пусть новый год принесёт много радости!", "gift": "⛄"},
    {"id": 3, "image": "🎁", "congratulation": "Здоровья, любви и исполнения желаний!", "gift": "🦌"},
    {"id": 4, "image": "🎁", "congratulation": "Процветания и успехов в новом году!", "gift": "🔔"},
    {"id": 5, "image": "🎁", "congratulation": "Мира, добра и уютных вечеров!", "gift": "❄️"},
    {"id": 6, "image": "🎁", "congratulation": "Пусть каждый день будет волшебным!", "gift": "🌟"},
    {"id": 7, "image": "🎁", "congratulation": "Тепла в доме и счастья в сердце!", "gift": "🕯️"},
    {"id": 8, "image": "🎁", "congratulation": "Новых достижений и ярких впечатлений!", "gift": "✨"},
    {"id": 9, "image": "🎁", "congratulation": "Благополучия и финансового роста!", "gift": "💰"},
    {"id": 10, "image": "🎁", "congratulation": "Крепкой дружбы и верной любви!", "gift": "💝"}
]

# Глобальное хранилище открытых подарков
opened_gifts = {}
SPECIAL_GIFTS = [7, 8, 9, 10]  # ID подарков только для авторизованных

# Главная страница лабы 9
@lab9.route('/lab9')
def index():
    return render_template('lab9/index.html')

# Страница авторизации/статуса
@lab9.route('/lab9/auth')
def auth_status():
    return render_template('lab9/auth.html',
                         is_authenticated=current_user.is_authenticated,
                         user_login=current_user.login if current_user.is_authenticated else 'Гость')

# Страница с подарками
@lab9.route('/lab9/newyear')
def newyear():
    # Генерируем случайные позиции для коробок
    user_id = get_user_id()
    random.seed(user_id)  # Фиксируем позиции для пользователя
    
    gifts_with_positions = []
    for i, gift in enumerate(GIFTS):
        gifts_with_positions.append({
            **gift,
            "top": random.randint(10, 80),
            "left": random.randint(5, 90),
            "opened": gift["id"] in opened_gifts.get(str(user_id), []),
            "special": gift["id"] in SPECIAL_GIFTS
        })
    
    # Получаем открытые подарки пользователя
    user_opened = opened_gifts.get(str(user_id), [])
    
    return render_template('lab9/newyear.html', 
                         gifts=gifts_with_positions,
                         opened_count=len(user_opened),
                         remaining=10 - len(user_opened),
                         is_authenticated=current_user.is_authenticated,
                         user_login=current_user.login if current_user.is_authenticated else 'Гость',
                         user_id=user_id)

# Открытие подарка
@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    data = request.json
    gift_id = data.get('gift_id')
    
    # Инициализируем сессию если нужно
    if 'opened_count' not in session:
        session['opened_count'] = 0
    
    # Проверяем лимит
    if session['opened_count'] >= 3:
        return jsonify({
            "success": False,
            "message": "Вы уже открыли максимальное количество подарков (3)!",
            "opened_count": session['opened_count']
        })
    
    # Проверяем доступ к специальным подаркам
    if gift_id in SPECIAL_GIFTS and not current_user.is_authenticated:
        return jsonify({
            "success": False,
            "message": "Этот подарок только для авторизованных пользователей! Войдите в систему.",
            "opened_count": session['opened_count']
        })
    
    # Проверяем, не открыт ли уже подарок
    user_id = get_user_id()
    if user_id not in opened_gifts:
        opened_gifts[user_id] = []
    
    if gift_id in opened_gifts[user_id]:
        return jsonify({
            "success": False,
            "message": "Этот подарок уже открыт!",
            "opened_count": session['opened_count']
        })
    
    # Находим подарок
    gift = next((g for g in GIFTS if g["id"] == gift_id), None)
    if not gift:
        return jsonify({
            "success": False,
            "message": "Подарок не найден!",
            "opened_count": session['opened_count']
        })
    
    # Открываем подарок
    opened_gifts[user_id].append(gift_id)
    session['opened_count'] += 1
    
    return jsonify({
        "success": True,
        "congratulation": gift["congratulation"],
        "gift": gift["gift"],
        "opened_count": session['opened_count'],
        "remaining": 10 - len(opened_gifts[user_id])
    })

# Сброс подарков для всех пользователей
@lab9.route('/lab9/reset')
def reset_gifts():
    user_id = get_user_id()
    if user_id in opened_gifts:
        opened_gifts[user_id] = []
    session['opened_count'] = 0
    return jsonify({"success": True})

# Режим Деда Мороза (только для авторизованных)
@lab9.route('/lab9/santa_mode')
@login_required
def santa_mode():
    user_id = str(current_user.id)
    if user_id in opened_gifts:
        opened_gifts[user_id] = []
    session['opened_count'] = 0
    return jsonify({
        "success": True,
        "message": "🎅 Дед Мороз наполнил все коробки заново! Подарки снова ждут вас!"
    })

# Получить ID пользователя
def get_user_id():
    """Получить ID пользователя (для гостей используем сессию)"""
    if current_user.is_authenticated:
        return str(current_user.id)
    else:
        # Для гостей используем уникальный ID из сессии
        if 'guest_id' not in session:
            session['guest_id'] = random.randint(1000, 9999)
        return f"guest_{session['guest_id']}"