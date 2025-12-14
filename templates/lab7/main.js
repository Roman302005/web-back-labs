// Функция для отображения сообщений
function showMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.style.display = 'block';
    
    if (isError) {
        element.className = 'error-message';
    } else {
        element.className = 'success-message';
    }
    
    // Автоматически скрыть сообщение через 5 секунд
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// Функция для загрузки и отображения списка фильмов
function fillFilmList() {
    const tbody = document.getElementById('film-list');
    
    // Показываем индикатор загрузки
    tbody.innerHTML = `
        <tr id="loading-row">
            <td colspan="4" class="loading">
                <div>Загрузка фильмов...</div>
            </td>
        </tr>
    `;
    
    fetch('/lab7/rest-api/films/')
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Ошибка сети: ' + response.status);
            }
            return response.json();
        })
        .then(function(films) {
            tbody.innerHTML = '';
            
            if (films.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="4" class="no-films">
                            Список фильмов пуст<br>
                            <small>Нажмите "Добавить фильм", чтобы создать первый фильм</small>
                        </td>
                    </tr>
                `;
                return;
            }
            
            films.forEach(function(film, index) {
                const tr = document.createElement('tr');
                
                // Ячейка с названием
                const titleCell = document.createElement('td');
                titleCell.className = 'film-title';
                titleCell.textContent = film.title_ru;
                
                // Ячейка с оригинальным названием (если отличается)
                const originalTitleCell = document.createElement('td');
                if (film.title !== film.title_ru) {
                    originalTitleCell.className = 'film-title-eng';
                    originalTitleCell.textContent = film.title;
                }
                
                // Ячейка с годом
                const yearCell = document.createElement('td');
                yearCell.innerHTML = `<span class="film-year">${film.year}</span>`;
                
                // Ячейка с кнопками действий
                const actionsCell = document.createElement('td');
                const actionsDiv = document.createElement('div');
                actionsDiv.className = 'action-buttons';
                
                // Кнопка редактирования
                const editButton = document.createElement('button');
                editButton.className = 'btn btn-edit';
                editButton.textContent = 'Редактировать';
                editButton.onclick = function() {
                    editFilm(index);
                };
                
                // Кнопка удаления
                const deleteButton = document.createElement('button');
                deleteButton.className = 'btn btn-delete';
                deleteButton.textContent = 'Удалить';
                deleteButton.onclick = function() {
                    deleteFilm(index, film.title_ru);
                };
                
                actionsDiv.appendChild(editButton);
                actionsDiv.appendChild(deleteButton);
                actionsCell.appendChild(actionsDiv);
                
                // Добавляем ячейки в строку
                tr.appendChild(titleCell);
                tr.appendChild(originalTitleCell);
                tr.appendChild(yearCell);
                tr.appendChild(actionsCell);
                
                // Добавляем строку в таблицу
                tbody.appendChild(tr);
            });
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке фильмов:', error);
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="error-message">
                        Ошибка загрузки данных<br>
                        <small>${error.message}</small>
                    </td>
                </tr>
            `;
            showMessage('error-message', 'Не удалось загрузить список фильмов. Проверьте соединение с сервером.', true);
        });
}

// Функция для удаления фильма
function deleteFilm(id, filmTitle) {
    if (confirm(`Вы уверены, что хотите удалить фильм "${filmTitle}"?`)) {
        fetch(`/lab7/rest-api/films/${id}`, {
            method: 'DELETE'
        })
        .then(function(response) {
            if (response.status === 204) {
                // Обновляем таблицу после удаления
                fillFilmList();
                showMessage('success-message', `Фильм "${filmTitle}" успешно удалён!`);
            } else if (response.status === 404) {
                showMessage('error-message', 'Фильм не найден!', true);
            } else {
                showMessage('error-message', 'Ошибка при удалении фильма!', true);
            }
        })
        .catch(function(error) {
            console.error('Ошибка при удалении фильма:', error);
            showMessage('error-message', 'Не удалось удалить фильм!', true);
        });
    }
}

// Функция для редактирования фильма
function editFilm(id) {
    // Получаем текущие данные фильма
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Фильм не найден');
            }
            return response.json();
        })
        .then(function(film) {
            // Создаем модальное окно для редактирования
            const modalHtml = `
                <div id="edit-modal" style="
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.7);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    z-index: 1000;
                ">
                    <div style="
                        background: white;
                        padding: 30px;
                        border-radius: 10px;
                        width: 90%;
                        max-width: 500px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    ">
                        <h2 style="color: #2c3e50; margin-bottom: 20px;">Редактировать фильм</h2>
                        
                        <div style="margin-bottom: 15px;">
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Название на русском:</label>
                            <input type="text" id="edit-title-ru" value="${film.title_ru}" style="
                                width: 100%;
                                padding: 10px;
                                border: 2px solid #ddd;
                                border-radius: 5px;
                                font-size: 16px;
                            ">
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Оригинальное название:</label>
                            <input type="text" id="edit-title" value="${film.title}" style="
                                width: 100%;
                                padding: 10px;
                                border: 2px solid #ddd;
                                border-radius: 5px;
                                font-size: 16px;
                            ">
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Год выпуска:</label>
                            <input type="number" id="edit-year" value="${film.year}" min="1900" max="2025" style="
                                width: 100%;
                                padding: 10px;
                                border: 2px solid #ddd;
                                border-radius: 5px;
                                font-size: 16px;
                            ">
                        </div>
                        
                        <div style="margin-bottom: 25px;">
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Описание:</label>
                            <textarea id="edit-description" rows="4" style="
                                width: 100%;
                                padding: 10px;
                                border: 2px solid #ddd;
                                border-radius: 5px;
                                font-size: 16px;
                                resize: vertical;
                            ">${film.description}</textarea>
                        </div>
                        
                        <div style="display: flex; justify-content: flex-end; gap: 10px;">
                            <button onclick="document.getElementById('edit-modal').remove()" style="
                                padding: 10px 20px;
                                background: #95a5a6;
                                color: white;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                            ">Отмена</button>
                            <button onclick="saveFilmEdit(${id})" style="
                                padding: 10px 20px;
                                background: #3498db;
                                color: white;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                            ">Сохранить</button>
                        </div>
                    </div>
                </div>
            `;
            
            // Добавляем модальное окно на страницу
            document.body.insertAdjacentHTML('beforeend', modalHtml);
        })
        .catch(function(error) {
            console.error('Ошибка при получении фильма:', error);
            showMessage('error-message', 'Не удалось загрузить данные фильма для редактирования!', true);
        });
}

// Функция для сохранения изменений фильма
function saveFilmEdit(id) {
    const updatedFilm = {
        title: document.getElementById('edit-title').value,
        title_ru: document.getElementById('edit-title-ru').value,
        year: parseInt(document.getElementById('edit-year').value),
        description: document.getElementById('edit-description').value
    };
    
    // Проверка обязательных полей
    if (!updatedFilm.title_ru.trim() || !updatedFilm.title.trim() || !updatedFilm.year) {
        alert('Пожалуйста, заполните все обязательные поля!');
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedFilm)
    })
    .then(function(response) {
        if (response.ok) {
            // Удаляем модальное окно
            document.getElementById('edit-modal').remove();
            
            // Обновляем таблицу
            fillFilmList();
            showMessage('success-message', 'Фильм успешно обновлён!');
        } else {
            showMessage('error-message', 'Ошибка при обновлении фильма!', true);
        }
    })
    .catch(function(error) {
        console.error('Ошибка при обновлении фильма:', error);
        showMessage('error-message', 'Не удалось обновить фильм!', true);
    });
}

// Функция для добавления нового фильма
function addFilm() {
    // Создаем модальное окно для добавления
    const modalHtml = `
        <div id="add-modal" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        ">
            <div style="
                background: white;
                padding: 30px;
                border-radius: 10px;
                width: 90%;
                max-width: 500px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            ">
                <h2 style="color: #2c3e50; margin-bottom: 20px;">Добавить новый фильм</h2>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Название на русском:*</label>
                    <input type="text" id="add-title-ru" placeholder="Например: Интерстеллар" style="
                        width: 100%;
                        padding: 10px;
                        border: 2px solid #ddd;
                        border-radius: 5px;
                        font-size: 16px;
                    " required>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Оригинальное название:*</label>
                    <input type="text" id="add-title" placeholder="Например: Interstellar" style="
                        width: 100%;
                        padding: 10px;
                        border: 2px solid #ddd;
                        border-radius: 5px;
                        font-size: 16px;
                    " required>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Год выпуска:*</label>
                    <input type="number" id="add-year" min="1900" max="2025" placeholder="2024" style="
                        width: 100%;
                        padding: 10px;
                        border: 2px solid #ddd;
                        border-radius: 5px;
                        font-size: 16px;
                    " required>
                </div>
                
                <div style="margin-bottom: 25px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Описание:*</label>
                    <textarea id="add-description" rows="4" placeholder="Краткое описание фильма..." style="
                        width: 100%;
                        padding: 10px;
                        border: 2px solid #ddd;
                        border-radius: 5px;
                        font-size: 16px;
                        resize: vertical;
                    " required></textarea>
                </div>
                
                <div style="display: flex; justify-content: flex-end; gap: 10px;">
                    <button onclick="document.getElementById('add-modal').remove()" style="
                        padding: 10px 20px;
                        background: #95a5a6;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    ">Отмена</button>
                    <button onclick="saveNewFilm()" style="
                        padding: 10px 20px;
                        background: #27ae60;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    ">Добавить</button>
                </div>
            </div>
        </div>
    `;
    
    // Добавляем модальное окно на страницу
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

// Функция для сохранения нового фильма
function saveNewFilm() {
    const newFilm = {
        title: document.getElementById('add-title').value,
        title_ru: document.getElementById('add-title-ru').value,
        year: parseInt(document.getElementById('add-year').value),
        description: document.getElementById('add-description').value
    };
    
    // Проверка обязательных полей
    if (!newFilm.title_ru.trim() || !newFilm.title.trim() || !newFilm.year || !newFilm.description.trim()) {
        alert('Пожалуйста, заполните все обязательные поля!');
        return;
    }
    
    fetch('/lab7/rest-api/films/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newFilm)
    })
    .then(function(response) {
        if (response.status === 201) {
            // Удаляем модальное окно
            document.getElementById('add-modal').remove();
            
            // Обновляем таблицу
            fillFilmList();
            showMessage('success-message', 'Фильм успешно добавлен!');
        } else {
            showMessage('error-message', 'Ошибка при добавлении фильма!', true);
        }
    })
    .catch(function(error) {
        console.error('Ошибка при добавлении фильма:', error);
        showMessage('error-message', 'Не удалось добавить фильм!', true);
    });
}