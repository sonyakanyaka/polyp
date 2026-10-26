import sqlite3

def check_medications(med_names):
    # Подключаемся к базе
    conn = sqlite3.connect("polypharmacy.db")
    conn.row_factory = sqlite3.Row # Чтобы обращаться к колонкам по имени
    cursor = conn.cursor()

    # 1. Находим ID введённых лекарств
    found_meds = []   # Список найденных лекарств (id, name)
    unknown_meds = [] # Список того, что не нашли
    
    for name in med_names:
        name = name.strip().lower()
        if not name:
            continue
            
        cursor.execute("SELECT id, name FROM active_ingredients WHERE name_lower = ?", (name,))
        row = cursor.fetchone()
        if row:
            # Добавляем, только если такого лекарства ещё нет в списке (чтобы не было дублей)
            if row["id"] not in [m["id"] for m in found_meds]:
                found_meds.append(row)
        else:
            unknown_meds.append(name)

    print("\n--- РАСПОЗНАННЫЕ ЛЕКАРСТВА ---")
    if found_meds:
        for m in found_meds:
            print(f"✅ {m['name']}")
    else:
        print("Ничего не распознано.")

    if unknown_meds:
        print("\n--- НЕ НАЙДЕНЫ В БАЗЕ ---")
        for m in unknown_meds:
            print(f"❓ {m}")

    print("\n--- ПРОВЕРКА НА ГЕРИАТРИЧЕСКИЕ РИСКИ (КРИТЕРИИ БИРСА) ---")
    beers_found = False
    for m in found_meds:
        cursor.execute("SELECT category, rationale, recommendation FROM beers_criteria WHERE ingredient_id = ?", (m["id"],))
        rules = cursor.fetchall()
        for rule in rules:
            beers_found = True
            print(f"⚠️ {m['name']} (Категория: {rule['category']})")
            print(f"   Почему: {rule['rationale']}")
            print(f"   Что делать: {rule['recommendation']}\n")
    
    if not beers_found:
        print("Явных рисков по критериям Бирса в нашей базе не найдено.")

    print("\n--- ПРОВЕРКА ВЗАИМОДЕЙСТВИЙ ---")
    interactions_found = False
    # Проверяем каждую пару лекарств
    for i in range(len(found_meds)):
        for j in range(i + 1, len(found_meds)):
            id1 = found_meds[i]["id"]
            id2 = found_meds[j]["id"]
            name1 = found_meds[i]["name"]
            name2 = found_meds[j]["name"]
            
            # Ищем взаимодействие (в любом порядке)
            cursor.execute("""
                SELECT severity, description FROM drug_interactions 
                WHERE (ingredient_id_1 = ? AND ingredient_id_2 = ?)
                   OR (ingredient_id_1 = ? AND ingredient_id_2 = ?)
            """, (id1, id2, id2, id1))
            
            rules = cursor.fetchall()
            for rule in rules:
                interactions_found = True
                print(f"🔴 {name1} + {name2} (Опасность: {rule['severity']})")
                print(f"   {rule['description']}\n")

    if not interactions_found:
        print("Опасных взаимодействий в нашей базе не найдено.")

    conn.close()

# --- ЗАПУСК ПРОГРАММЫ ---
if __name__ == "__main__":
    print("Введите названия лекарств через запятую.")
    print("Например: ибупрофен, варфарин, диазепам")
    user_input = input("\nВаш список: ")
    
    # Разбиваем строку по запятым и убираем лишние пробелы
    meds_list = [m.strip() for m in user_input.split(",") if m.strip()]
    
    if meds_list:
        check_medications(meds_list)
    else:
        print("Вы ничего не ввели.")