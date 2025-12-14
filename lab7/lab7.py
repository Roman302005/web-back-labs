from flask import Blueprint, render_template, jsonify, abort, request

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

# База данных фильмов в памяти
films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений заставляют человечество бороться за выживание, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника."
    },
    {
        "title": "The Godfather",
        "title_ru": "Крёстный отец",
        "year": 1972,
        "description": "Криминальная сага о нью-йоркской сицилийской мафиозной семье Корлеоне."
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Тёмный рыцарь",
        "year": 2008,
        "description": "Бэтмен поднимает ставки в войне с преступностью."
    },
    {
        "title": "Pulp Fiction",
        "title_ru": "Криминальное чтиво",
        "year": 1994,
        "description": "Истории о жизни нескольких мелких преступников, наркоманов, гангстеров."
    }
]

# Вспомогательная функция для обработки названий
def process_film_data(film_data):
    """Обрабатывает данные фильма: если оригинальное название пустое, 
       использует русское название"""
    processed_data = film_data.copy()
    
    # Если оригинальное название пустое, а русское задано
    if not processed_data.get('title', '').strip() and processed_data.get('title_ru', '').strip():
        processed_data['title'] = processed_data['title_ru']
    
    # Если русское название пустое, а оригинальное задано
    if not processed_data.get('title_ru', '').strip() and processed_data.get('title', '').strip():
        processed_data['title_ru'] = processed_data['title']
    
    # Преобразуем год в число
    if 'year' in processed_data:
        try:
            processed_data['year'] = int(processed_data['year'])
        except (ValueError, TypeError):
            processed_data['year'] = 0
    
    return processed_data

# Получение всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

# Получение конкретного фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с ID {id} не найден")
    return jsonify(films[id])

# Удаление фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с ID {id} не найден")
    del films[id]
    return '', 204

# Редактирование существующего фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с ID {id} не найден")
    
    film_data = request.get_json()
    if not film_data:
        abort(400, description="Отсутствуют данные для обновления")
    
    # Обрабатываем данные фильма
    processed_data = process_film_data(film_data)
    
    # Обновляем фильм
    films[id] = processed_data
    return jsonify(films[id]), 200

# Добавление нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()
    if not film_data:
        abort(400, description="Отсутствуют данные для создания фильма")
    
    # Проверяем обязательные поля
    if not film_data.get('title_ru', '').strip() and not film_data.get('title', '').strip():
        abort(400, description="Необходимо указать хотя бы одно название фильма")
    
    if 'year' not in film_data:
        abort(400, description="Не указан год выпуска")
    
    # Обрабатываем данные фильма
    processed_data = process_film_data(film_data)
    
    # Добавляем новый фильм
    films.append(processed_data)
    new_id = len(films) - 1
    
    return jsonify({
        "id": new_id,
        "message": "Фильм успешно добавлен",
        "film": processed_data
    }), 201