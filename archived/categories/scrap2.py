from lxml import html
import json

with open('./categories.html', 'r', encoding='utf-8') as f:
    tree = html.fromstring(f.read())

def parse_li(li):
    # Берем первую ссылку внутри li (она всегда главная для этой категории)
    a = li.xpath('./a')[0] if li.xpath('./a') else None
    if a is None:
        return None

    item = {"name": a.text_content().strip()}

    # Если есть вложенный ul — уходим вглубь
    ul = li.xpath('./ul')
    if ul:
        subcategories = []
        for sub_li in ul[0].xpath('./li'):
            parsed = parse_li(sub_li)
            if parsed:
                subcategories.append(parsed)
        if subcategories:
            item["subcategories"] = subcategories
    else:
        href = a.get("href")
        if href:
            item["link"] = href

    return item

def get_categories(tree):
    categories = []
    ul_menu = tree.cssselect('.m-menu-left')
    if ul_menu:
        for li in ul_menu[0].xpath('./li'):
            parsed = parse_li(li)
            if parsed:
                categories.append(parsed)
    return categories

output = get_categories(tree)

with open('cats_levels.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print(json.dumps(output, ensure_ascii=False, indent=2))
