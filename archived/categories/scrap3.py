from lxml import html
import json

with open('./categories.html', 'r', encoding='utf-8') as f:
    tree = html.fromstring(f.read())

def parse_li(li, level=1, parent_name=None):
    # Берем первую ссылку внутри li
    a_nodes = li.xpath('./a')
    if not a_nodes:
        return None
    a = a_nodes[0]

    name = a.text_content().strip()
    href = a.get("href")

    # если мы на уровне 2 → проверяем, есть ли подкатегории (ур.3)
    if level == 2:
        ul = li.xpath('./ul')
        if ul:
            # разворачиваем подкатегории в плоский список
            items = []
            for sub_li in ul[0].xpath('./li'):
                sub_a_nodes = sub_li.xpath('./a')
                if not sub_a_nodes:
                    continue
                sub_a = sub_a_nodes[0]
                items.append({
                    "name": f"{name}: {sub_a.text_content().strip()}",
                    "link": sub_a.get("href")
                })
            return items
        else:
            return {"name": name, "link": href}

    # если уровень 1 → классическая схема: name + subcategories
    item = {"name": name}
    ul = li.xpath('./ul')
    if ul:
        subcategories = []
        for sub_li in ul[0].xpath('./li'):
            parsed = parse_li(sub_li, level=level+1, parent_name=name)
            if parsed:
                if isinstance(parsed, list):
                    subcategories.extend(parsed)
                else:
                    subcategories.append(parsed)
        if subcategories:
            item["subcategories"] = subcategories
    else:
        if href:
            item["link"] = href

    return item


def get_categories(tree):
    categories = []
    ul_menu = tree.cssselect('.m-menu-left')
    if ul_menu:
        for li in ul_menu[0].xpath('./li'):
            parsed = parse_li(li, level=1)
            if parsed:
                if isinstance(parsed, list):
                    categories.extend(parsed)
                else:
                    categories.append(parsed)
    return categories


output = get_categories(tree)

with open('cats_no_level.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print(json.dumps(output, ensure_ascii=False, indent=2))
