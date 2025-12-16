import os
import sqlite3
from app import app

print("🚀 Создаю таблицы с нуля...")

# 1. Удаляем старую базу если есть
if os.path.exists('database.db'):
    os.remove('database.db')
    print("✅ Удалил старую базу данных")
else:
    print("✅ Старой базы не было, создаю новую")

# 2. Создаем новую базу SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 3. Создаем таблицу users
try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    print("✅ Таблица users создана/проверена")
except Exception as e:
    print(f"❌ Ошибка при создании users: {e}")

# 4. Создаем таблицу articles с колонкой content
try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER
    )
    ''')
    print("✅ Таблица articles создана с колонкой content")
except Exception as e:
    print(f"❌ Ошибка при создании articles: {e}")

conn.commit()

# 5. Показываем структуру таблиц
print("\n📊 Проверяю структуру таблиц:")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"✅ Найдено таблиц: {len(tables)}")

for table_name in tables:
    print(f"\n📋 Таблица: {table_name[0]}")
    cursor.execute(f"PRAGMA table_info({table_name[0]})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

conn.close()

print("\n" + "="*50)
print("✅ База данных успешно создана!")
print("📋 Структура:")
print("   Таблица 'users': id, login, password")
print("   Таблица 'articles': id, title, content, user_id")
print("\n🎯 Теперь запустите сервер:")
print("   python app.py")