from parser import Parser
import json
import math

parser = Parser()

with open('./categories.json', 'r', encoding='utf-8') as cats_file:
    cats = json.load(cats_file)

    for cat in cats:
        cat_name = cat['name']
        print(f"Новая категория \"{cat_name}\"")
        subcats = cat['subcategories']

        for subcat in subcats:
            subcat_name = subcat['name']
            print(f"Новая под-категория \"{subcat_name}\"")
            subcat_link = subcat['link']

            _, _, total = parser.get96cards(subcat_link, 1)

            if not total:
                print(f"Не удалось получить кол-во карточек (\"{cat_name}\" -> \"{subcat_name}\")")
                continue

            pages_count = math.ceil(total / 96)

            for page in range(1, pages_count+1):
                print(f"(\"{cat_name}\" -> \"{subcat_name}\" -> {page}/{pages_count})")

                cards, shown, total = parser.get96cards(subcat_link, page)

                if not cards:
                    print(f"Не удалось получить карточки (\"{cat_name}\" -> \"{subcat_name}\" -> {page}/{pages_count})")
                
                for card in cards:
                    pass # Добавляем в таблицу
                    print(card["title"][:15])
                
                print(f"В таблицу добавлено {len(cards)}")
