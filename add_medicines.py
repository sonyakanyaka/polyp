import sqlite3

# Подключаемся к нашей базе
conn = sqlite3.connect("polypharmacy.db")
cursor = conn.cursor()

# 1. Добавляем сами лекарства (действующие вещества)
# Формат: (Название как показываем, название в нижнем регистре для поиска)
medicines = [
    ("Ибупрофен", "ибупрофен"),
    ("Варфарин", "варфарин"),
    ("Диазепам", "диазепам"),
    ("Амитриптилин", "амитриптилин"),
    ("Спиронолактон", "спиронолактон"),
    ("Эналаприл", "эналаприл")
]

for name, name_lower in medicines:
    # Проверяем, нет ли уже такого лекарства, чтобы не было ошибки
    cursor.execute("SELECT id FROM active_ingredients WHERE name_lower = ?", (name_lower,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO active_ingredients (name, name_lower) VALUES (?, ?)",
            (name, name_lower)
        )
        print(f"Добавлено лекарство: {name}")

# 2. Добавляем правила Бирса (гериатрические риски)
# Находим ID лекарств, чтобы привязать к ним правила
def get_id(name_lower):
    cursor.execute("SELECT id FROM active_ingredients WHERE name_lower = ?", (name_lower,))
    row = cursor.fetchone()
    return row[0] if row else None

diazepam_id = get_id("диазепам")
amitriptyline_id = get_id("амитриптилин")

if diazepam_id:
    cursor.execute(
        "INSERT INTO beers_criteria (ingredient_id, category, rationale, recommendation, source) VALUES (?, ?, ?, ?, ?)",
        (diazepam_id, "Avoid", "Бензодиазепины повышают риск когнитивных нарушений, делирия, падений и переломов у пожилых.", "Обсудите риски с врачом. Резко не отменяйте препарат.", "AGS Beers Criteria 2023")
    )
    print("Добавлено правило Бирса для Диазепама")

if amitriptyline_id:
    cursor.execute(
        "INSERT INTO beers_criteria (ingredient_id, category, rationale, recommendation, source) VALUES (?, ?, ?, ?, ?)",
        (amitriptyline_id, "Avoid", "Выраженное антихолинергическое действие: спутанность сознания, сухость во рту, задержка мочи.", "Обсудите с врачом альтернативы.", "AGS Beers Criteria 2023")
    )
    print("Добавлено правило Бирса для Амитриптилина")

# 3. Добавляем взаимодействия (варфарин + ибупрофен, спиронолактон + эналаприл)
warfarin_id = get_id("варфарин")
ibuprofen_id = get_id("ибупрофен")
spironolactone_id = get_id("спиронолактон")
enalapril_id = get_id("эналаприл")

if warfarin_id and ibuprofen_id:
    cursor.execute(
        "INSERT INTO drug_interactions (ingredient_id_1, ingredient_id_2, severity, description, source) VALUES (?, ?, ?, ?, ?)",
        (warfarin_id, ibuprofen_id, "major", "Повышенный риск кровотечения. НПВС нарушают свертываемость и повреждают слизистую ЖКТ.", "Официальные инструкции")
    )
    print("Добавлено взаимодействие: Варфарин + Ибупрофен")

if spironolactone_id and enalapril_id:
    cursor.execute(
        "INSERT INTO drug_interactions (ingredient_id_1, ingredient_id_2, severity, description, source) VALUES (?, ?, ?, ?, ?)",
        (spironolactone_id, enalapril_id, "moderate", "Риск повышения уровня калия в крови (гиперкалиемия).", "Официальные инструкции")
    )
    print("Добавлено взаимодействие: Спиронолактон + Эналаприл")

# Сохраняем изменения
conn.commit()
conn.close()

print("\n✅ Данные успешно добавлены в базу!")