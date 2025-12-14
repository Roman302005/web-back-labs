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

# Получение всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

# Получение конкретного фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    # Проверка на выход за границы списка
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с ID {id} не найден")
    
    return jsonify(films[id])

# Удаление фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    # Проверка на выход за границы списка
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с ID {id} не найден")
    
    # Удаляем фильм из списка
    del films[id]
    
    # Возвращаем пустой ответ с кодом 204 No Content
    return '', 204

# Редактирование существующего фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    # Проверка на выход за границы списка
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с ID {id} не найден")
    
    # Получаем данные из запроса (JSON)
    film_data = request.get_json()
    
    # Проверяем, что данные получены
    if not film_data:
        abort(400, description="Отсутствуют данные для обновления")
    
    # Обновляем фильм
    films[id] = film_data
    
    # Возвращаем обновлённый фильм
    return jsonify(films[id]), 200

# Добавление нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    # Получаем данные из запроса (JSON)
    film_data = request.get_json()
    
    # Проверяем, что данные получены
    if not film_data:
        abort(400, description="Отсутствуют данные для создания фильма")
    
    # Проверяем обязательные поля
    required_fields = ['title', 'title_ru', 'year', 'description']
    for field in required_fields:
        if field not in film_data:
            abort(400, description=f"Отсутствует обязательное поле: {field}")
    
    # Добавляем новый фильм в конец списка
    films.append(film_data)
    
    # Возвращаем ID нового фильма (индекс последнего элемента)
    new_id = len(films) - 1
    
    # Обычно при POST возвращают созданный объект или его ID
    # Можно вернуть как сам фильм, так и его ID
    return jsonify({
        "id": new_id,
        "message": "Фильм успешно добавлен",
        "film": film_data
    }), 201  # 201 Created - стандартный код для успешного создания