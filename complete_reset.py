import sqlite3

print("🔧 Добавляю колонку content в таблицу articles...")

try:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Проверяем, есть ли колонка content
    cursor.execute("PRAGMA table_info(articles)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'content' not in columns:
        # Добавляем колонку content
        cursor.execute("ALTER TABLE articles ADD COLUMN content TEXT")
        print("✅ Добавил колонку content в таблицу articles")
        
        # Обновляем существующие записи (если есть)
        cursor.execute("UPDATE articles SET content = 'Текст статьи' WHERE content IS NULL")
        print("✅ Обновил существующие записи")
    else:
        print("✅ Колонка content уже существует")
    
    conn.commit()
    conn.close()
    
    # Проверяем
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(articles)")
    print("\n📊 Структура таблицы articles:")
    for col in cursor.fetchall():
        print(f"  - {col[1]} ({col[2]})")
    conn.close()
    
    print("\n✅ Готово! Перезапустите сервер.")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("Попробуйте Решение 1 (полный сброс)")