import os
import sqlite3

print("🎯 Простое создание базы данных...")

# Удаляем если есть
if os.path.exists('database.db'):
    os.remove('database.db')
    print("🗑️  Удалил старую базу")

# Создаем новую
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Таблица пользователей
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Таблица статей - ВАЖНО: колонка называется content
cursor.execute('''
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    user_id INTEGER
)
''')

conn.commit()

# Добавляем тестового пользователя
cursor.execute(
    "INSERT INTO users (login, password) VALUES (?, ?)",
    ('test', 'pbkdf2:sha256:260000$...тестовый хеш...')
)

conn.commit()
conn.close()

print("✅ База данных создана!")
print("✅ Таблица 'articles' создана с колонкой 'content'")
print("✅ Добавлен тестовый пользователь 'test'")

# Показать структуру
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("\n📋 Структура таблицы 'articles':")
cursor.execute("PRAGMA table_info(articles)")
for col in cursor.fetchall():
    print(f"  - {col[1]} ({col[2]})")

conn.close()

print("\n🎉 Теперь запустите: python app.py")