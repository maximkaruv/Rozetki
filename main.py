import json
import csv
import os
from parser import Parser


CSV_FILE = "cards.csv"


def save_cards_to_csv(cards, category_name, subcategory_name, filename=CSV_FILE):
    """Сохраняет список карточек в CSV, добавляя категорию и подкатегорию"""
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["category", "subcategory", "image", "title", "serial", "price"]
        )

        # Записываем заголовки только если файл создаётся впервые
        if not file_exists:
            writer.writeheader()

        for card in cards:
            writer.writerow({
                "category": category_name,
                "subcategory": subcategory_name,
                "image": "https://schneider-russia.com" + card["image"],
                "title": card["title"],
                "serial": card["serial"],
                "price": card["price"]
            })


def process_page(parser, category_name, subcategory_name, link, page):
    cards, total_pages, fully_parsed = parser.get_cards(link, page)
    if not cards:
        return False
    
    #print(cards)

    # Сохраняем в CSV
    save_cards_to_csv(cards, category_name, subcategory_name)

    print(f"В таблицу занесено {len(cards)} карточек по пути {category_name}/{subcategory_name}")

    if fully_parsed:
        print(f"Под-категория {category_name} полностью получена")
        return True

    return False


def process_subcategory(parser, category_name, subcategory):
    subcat_name = subcategory["name"]
    subcat_link = subcategory["link"]

    print(f"Текущая под-категория: {subcat_name}")

    # Первая страница
    fully_parsed = process_page(parser, category_name, subcat_name, subcat_link, 1)
    if fully_parsed:
        return

    # Остальные страницы
    _, total_pages, _ = parser.get_cards(subcat_link, 1)
    print(total_pages)
    for page in range(2, total_pages + 1):
        fully_parsed = process_page(parser, category_name, subcat_name, subcat_link, page)
        if fully_parsed:
            break


def main() -> None:
    parser = Parser()

    with open("categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    for category in categories:
        category_name = category["name"]
        print(f"Текущая категория: {category_name}")

        for subcategory in category["subcategories"]:
            process_subcategory(parser, category_name, subcategory)


if __name__ == "__main__":
    main()
