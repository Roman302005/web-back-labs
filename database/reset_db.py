import os
import sqlite3

# Удаляем старую базу если есть
if os.path.exists('database.db'):
    os.remove('database.db')
    print("✅ Старая база удалена")

# Создаем новую
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Таблица пользователей - САМАЯ ПРОСТАЯ ВЕРСИЯ
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Таблица статей
cursor.execute('''
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    user_id INTEGER
)
''')

conn.commit()
conn.close()
print("✅ Новая база создана с простой структурой")