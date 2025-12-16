import sqlite3
import os

print("🔍 ПРОВЕРКА БАЗЫ ДАННЫХ 🔍")

if not os.path.exists('database.db'):
    print("❌ Файл database.db не найден!")
    exit()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Проверяем таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print(f"✅ Найдено таблиц: {len(tables)}")
for table in tables:
    print(f"\n📋 Таблица: {table[0]}")
    
    # Показываем колонки
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    
    if table[0] == 'articles':
        has_content = False
        for col in columns:
            print(f"  ├ {col[1]} ({col[2]})")
            if col[1] == 'content':
                has_content = True
        
        if not has_content:
            print("\n❌❌❌ КРИТИЧЕСКАЯ ОШИБКА!")
            print("В таблице 'articles' НЕТ колонки 'content'!")
            print("Нужно пересоздать базу через hard_reset.py")
        else:
            print("\n✅ В таблице 'articles' ЕСТЬ колонка 'content'")
    
    else:
        for col in columns:
            print(f"  ├ {col[1]} ({col[2]})")

# Показываем содержимое
print("\n📊 Содержимое таблиц:")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"  ├ {table[0]}: {count} записей")

conn.close()

print("\n" + "="*60)
print("✅ Проверка завершена")