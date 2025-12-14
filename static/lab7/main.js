// Функция для показа сообщений
function showAlert(message, type = 'success') {
    const alertEl = document.getElementById('alert-message');
    alertEl.textContent = message;
    alertEl.className = `alert alert-${type}`;
    alertEl.style.display = 'block';
    
    // Автоматически скрыть через 5 секунд
    setTimeout(() => {
        alertEl.style.display = 'none';
    }, 5000);
}

// Функция для загрузки и отображения списка фильмов
function fillFilmList() {
    const tbody = document.getElementById('film-list');
    
    // Показываем индикатор загрузки
    tbody.innerHTML = `
        <tr>
            <td colspan="3" style="text-align: center; padding: 40px; color: #7f8c8d;">
                Загрузка фильмов...
            </td>
        </tr>
    `;
    
    fetch('/lab7/rest-api/films/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка загрузки данных');
            }
            return response.json();
        })
        .then(films => {
            tbody.innerHTML = '';
            
            if (films.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="3" style="text-align: center; padding: 40px; color: #95a5a6;">
                            Фильмов пока нет. Нажмите "Добавить новый фильм", чтобы добавить первый фильм.
                        </td>
                    </tr>
                `;
                return;
            }
            
            films.forEach((film, index) => {
                const tr = document.createElement('tr');
                
                // Ячейка с названием фильма
                const titleCell = document.createElement('td');
                const titleDiv = document.createElement('div');
                titleDiv.className = 'film-info';
                
                // Русское название (главное)
                const titleRu = document.createElement('div');
                titleRu.className = 'film-title-ru';
                titleRu.textContent = film.title_ru;
                
                // Оригинальное название (второстепенное, в скобках)
                if (film.title && film.title !== film.title_ru) {
                    const titleOriginal = document.createElement('div');
                    titleOriginal.className = 'film-title-original';
                    titleOriginal.textContent = film.title;
                    titleDiv.appendChild(titleRu);
                    titleDiv.appendChild(titleOriginal);
                } else {
                    titleDiv.appendChild(titleRu);
                }
                
                titleCell.appendChild(titleDiv);
                
                // Ячейка с годом
                const yearCell = document.createElement('td');
                const yearSpan = document.createElement('span');
                yearSpan.className = 'film-year';
                yearSpan.textContent = film.year;
                yearCell.appendChild(yearSpan);
                
                // Ячейка с действиями
                const actionsCell = document.createElement('td');
                const actionsDiv = document.createElement('div');
                actionsDiv.className = 'action-buttons';
                
                // Кнопка редактирования
                const editButton = document.createElement('button');
                editButton.className = 'btn btn-edit';
                editButton.innerHTML = '✏️ Редакт.';
                editButton.onclick = () => editFilm(index);
                
                // Кнопка удаления
                const deleteButton = document.createElement('button');
                deleteButton.className = 'btn btn-delete';
                deleteButton.innerHTML = '🗑️ Удалить';
                deleteButton.onclick = () => deleteFilm(index, film.title_ru);
                
                actionsDiv.appendChild(editButton);
                actionsDiv.appendChild(deleteButton);
                actionsCell.appendChild(actionsDiv);
                
                // Добавляем ячейки в строку
                tr.appendChild(titleCell);
                tr.appendChild(yearCell);
                tr.appendChild(actionsCell);
                
                // Добавляем строку в таблицу
                tbody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке фильмов:', error);
            tbody.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align: center; padding: 40px; color: #e74c3c;">
                        Ошибка загрузки данных. Проверьте соединение с сервером.
                    </td>
                </tr>
            `;
        });
}

// Функция для удаления фильма
function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }

    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            fillFilmList();
            showAlert(`Фильм "${title}" успешно удалён!`, 'success');
        } else {
            showAlert('Ошибка при удалении фильма', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка при удалении фильма:', error);
        showAlert('Не удалось удалить фильм', 'error');
    });
}

// Функция для редактирования фильма
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(response => response.json())
        .then(film => {
            document.getElementById('film-id').value = id;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('title').value = film.title !== film.title_ru ? film.title : '';
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            
            document.getElementById('modal-title').textContent = 'Редактировать фильм';
            showModal();
        })
        .catch(error => {
            console.error('Ошибка при получении фильма:', error);
            showAlert('Не удалось загрузить данные фильма', 'error');
        });
}

// Функция для добавления нового фильма
function addFilm() {
    document.getElementById('film-id').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('title').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    
    document.getElementById('modal-title').textContent = 'Добавить фильм';
    showModal();
}

// Функция для отправки фильма
function sendFilm() {
    const filmId = document.getElementById('film-id').value;
    const titleRu = document.getElementById('title-ru').value.trim();
    const titleOriginal = document.getElementById('title').value.trim();
    const year = document.getElementById('year').value;
    const description = document.getElementById('description').value.trim();

    // Валидация
    if (!titleRu) {
        showAlert('Пожалуйста, укажите русское название фильма', 'error');
        return;
    }
    
    if (!year) {
        showAlert('Пожалуйста, укажите год выпуска', 'error');
        return;
    }
    
    const film = {
        title_ru: titleRu,
        title: titleOriginal,
        year: parseInt(year),
        description: description
    };

    let url, method;
    
    if (filmId) {
        url = `/lab7/rest-api/films/${filmId}`;
        method = 'PUT';
    } else {
        url = '/lab7/rest-api/films/';
        method = 'POST';
    }

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(film)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(text || 'Ошибка сервера');
            });
        }
        return response.json();
    })
    .then(data => {
        fillFilmList();
        hideModal();
        
        if (filmId) {
            showAlert('Фильм успешно обновлён!', 'success');
        } else {
            showAlert('Фильм успешно добавлен!', 'success');
        }
    })
    .catch(error => {
        console.error('Ошибка при сохранении фильма:', error);
        showAlert(`Ошибка: ${error.message}`, 'error');
    });
}

// Функции для работы с модальным окном
function showModal() {
    document.getElementById('film-modal').style.display = 'flex';
}

function hideModal() {
    document.getElementById('film-modal').style.display = 'none';
}

function cancel() {
    hideModal();
}