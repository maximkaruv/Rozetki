import json

# Читаем старый конфиг
with open("old_cats.json", "r", encoding="utf-8") as f:
    old_config = json.load(f)

new_config = []

for category in old_config:
    for cat_name, subcats in category.items():
        new_config.append({
            "name": cat_name,
            "subcategories": subcats
        })

# Сохраняем новый конфиг
with open("new_cats.json", "w", encoding="utf-8") as f:
    json.dump(new_config, f, ensure_ascii=False, indent=4)

print("Конфиг успешно переформатирован в новый формат!")
