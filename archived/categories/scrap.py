from lxml import html
import json

with open('./categories.html', 'r', encoding='utf-8') as f:
    html_ = f.read()
    tree = html.fromstring(html_)

with open('categories.json', 'w', encoding='utf-8') as f:
    output = []

    for category in tree.cssselect('.m-menu-left > .m-menu-item'):
        name = category.cssselect('.m-menu-link')[0].text_content()
        subcats = []
        for subcategory in category.cssselect('.m-submenu-item'):
            card = subcategory.cssselect('.m-submenu-link')
            if card:
                card = card[0]
            else:
                continue

            subname = card.text_content()
            sublink = card.get('href')
            subcats.append({
                "name": subname,
                "link": sublink
            })
        output.append({
            name: subcats
        })

    json.dump(output, f, indent=2, ensure_ascii=False)