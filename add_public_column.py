import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Проверяем, есть ли колонка is_public
cursor.execute("PRAGMA table_info(articles)")
columns = [col[1] for col in cursor.fetchall()]

if 'is_public' not in columns:
    cursor.execute("ALTER TABLE articles ADD COLUMN is_public BOOLEAN DEFAULT 1")
    print("✅ Добавил колонку is_public в таблицу articles")
else:
    print("✅ Колонка is_public уже есть")

conn.commit()
conn.close()

# Проверяем
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(articles)")
print("\n📊 Структура articles:")
for col in cursor.fetchall():
    print(f"  - {col[1]} ({col[2]})")
conn.close()