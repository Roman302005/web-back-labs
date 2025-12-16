import os
import shutil
import sqlite3

print("💥 НАЧИНАЮ ПОЛНЫЙ СБРОС С ОЧИСТКОЙ КЕША 💥")

# 1. Удаляем ВСЁ что связано с базой
files_to_delete = [
    'database.db',
    'database.db-journal',
    'database.db-wal',
    'database.db-shm',
    'test.db',
    'test.db-journal',
    'test.db-wal',
    'test.db-shm',
    'flask_session',
    '.flask_session',
    'session.sqlite',
    'instance',
]

print("🗑️ Удаляю файлы баз данных...")
for file in files_to_delete:
    if os.path.exists(file):
        try:
            if os.path.isdir(file):
                shutil.rmtree(file)
                print(f"  ✅ Удалил папку: {file}")
            else:
                os.remove(file)
                print(f"  ✅ Удалил файл: {file}")
        except Exception as e:
            print(f"  ⚠️ Не удалось удалить {file}: {e}")

# 2. Удаляем папки __pycache__ везде
print("\n🗑️ Очищаю кеш Python...")
for root, dirs, files in os.walk('.'):
    for dir_name in dirs:
        if dir_name == '__pycache__':
            cache_dir = os.path.join(root, dir_name)
            try:
                shutil.rmtree(cache_dir)
                print(f"  ✅ Удалил кеш: {cache_dir}")
            except:
                pass

# 3. Создаем новую базу с нуля
print("\n🛠️ Создаю новую базу данных...")
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
print("  ✅ Создал таблицу 'users'")

# Таблица статей - колонка content!
cursor.execute('''
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    user_id INTEGER
)
''')
print("  ✅ Создал таблицу 'articles' с колонкой 'content'")

conn.commit()

# 4. Показываем что создалось
print("\n📊 Проверяю структуру:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

for table in tables:
    print(f"\n📋 Таблица: {table[0]}")
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  ├ {col[1]} ({col[2]}) {'NOT NULL' if col[3] else ''}")

conn.close()

print("\n" + "="*60)
print("✅ ПОЛНЫЙ СБРОС ВЫПОЛНЕН!")
print("📋 Структура базы:")
print("   Таблица 'users': id, login, password")
print("   Таблица 'articles': id, title, content, user_id")
print("\n🚀 Теперь:")
print("   1. ЗАКРОЙТЕ ВСЕ ОКНА ТЕРМИНАЛА")
print("   2. Откройте новый терминал")
print("   3. python app.py")
print("   4. http://localhost:5000/lab8/register")
print("="*60)