import os
from app import app
from database import db

print("🧹 Начинаю полный сброс через SQLAlchemy...")

# 1. Удаляем старую базу
if os.path.exists('database.db'):
    os.remove('database.db')
    print("✅ Удалил старую базу данных")

# 2. Создаем новую базу через SQLAlchemy
with app.app_context():
    # Создаем все таблицы
    db.create_all()
    print("✅ Все таблицы созданы через SQLAlchemy")
    
    # Проверяем через SQLite напрямую
    import sqlite3
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Показываем таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\n📊 Таблицы в базе данных:")
    for table in tables:
        print(f"  - {table[0]}")
        
        # Показываем колонки
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"    * {col[1]} ({col[2]})")
    
    conn.close()
    
    print("\n" + "="*50)
    print("✅ Готово! Запускайте сервер:")
    print("   python app.py")