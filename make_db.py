import sqlite3
from pathlib import Path

# Находим файл schema.sql в той же папке
schema_path = Path(__file__).parent / "schema.sql"

if not schema_path.exists():
    print("ОШИБКА: Файл schema.sql не найден рядом с make_db.py!")
    print(f"Искал здесь: {schema_path}")
else:
    # Читаем SQL-код и создаём базу
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_code = f.read()
    
    conn = sqlite3.connect("polypharmacy.db")
    conn.executescript(sql_code)
    conn.commit()
    
    # Проверяем, что таблицы создались
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print("OK: база создана!")
    print("Таблицы в базе:", tables)
    conn.close()