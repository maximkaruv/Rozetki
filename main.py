from parser import Parser
from table import CsvTable
import json
import math

parser = Parser()
table = CsvTable('cards.csv', ['Категория', 'Название', 'Цена', 'Бренд'])

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

            total = parser.getpages(subcat_link)

            if not total:
                print(f"Не удалось получить кол-во карточек (\"{cat_name}\" -> \"{subcat_name}\")")
                continue

            pages_count = math.ceil(total / 96)
            print(f"Кол-во страниц: {pages_count}")

            for page in range(1, pages_count+1):
                print(f"(\"{cat_name}\" -> \"{subcat_name}\" -> {page}/{pages_count})")

                cards = parser.get96cards(subcat_link, page)

                print(cards)
                continue

                if not cards:
                    print(f"Не удалось получить карточки (\"{cat_name}\" -> \"{subcat_name}\" -> {page}/{pages_count})")
                
                for card in cards:
                    pass # Добавляем в таблицу
                    print(card["title"][:15])
                
                print(f"В таблицу добавлено {len(cards)}")
