import requests
from lxml import html
from lxml.html import HtmlElement
import re


class Tree:
    def __init__(self, content):
        # если передали строку HTML
        if isinstance(content, str):
            self.tree = html.fromstring(content)
        # если передали lxml-элемент
        elif isinstance(content, HtmlElement):
            self.tree = content
        else:
            raise ValueError("Tree может принимать только строку HTML или lxml-элемент")

    # Получение элемента по css-селектору
    def select(self, selector):
        elements = self.tree.cssselect(selector)

        class Elements:
            def __init__(self, elements):
                self.elements = elements

            def text(self, index=0, default=""):
                try:
                    return self.elements[index].text_content().strip()
                except IndexError:
                    return default

            def attr(self, name, index=0, default=""):
                try:
                    return self.elements[index].get(name, default)
                except IndexError:
                    return default

            def __getitem__(self, idx):
                return self.elements[idx]

            def __iter__(self):
                return iter(self.elements)

            def __len__(self):
                return len(self.elements)

        return Elements(elements)


class Parser:
    def __init__(self):
        pass

    # Получаем HTML разметку по ссылке
    def getpage(self, link):
        res = requests.get(link)
        res.raise_for_status()
        with open('last-fetch.html', 'w', encoding='utf-8') as file:
            file.write(res.text)
        return res.text

    # Получаем список карточек товаров по категории и странице
    def get96cards(self, category, page):
        try:
            content = self.getpage(
                f"https://schneider-russia.com{category}?order=viewed&onpage=96&page={page}"
            )
            tree = Tree(content)

            # Получаем доп.информацию
            info = tree.select('.category-counter').text(1)
            match = re.findall(r"(\d+)", info)
            if match and len(match) == 2:
                shown, total = map(int, match)
            else:
                print("Доп. информация не найдена")
                shown, total = None, None

            # Получаем список карточек
            cards_elems = tree.select('.grid-products > li')
            if len(cards_elems) == 0:
                print("Карточки не найдены")
                return (None, shown, total)

            cards = []
            for card in cards_elems:
                try:
                    subtree = Tree(html.tostring(card))

                    image = subtree.select('.category-item-image > img').attr("src")
                    title = subtree.select('.category-item-title').text()
                    serial = subtree.select('.category-item-brand').text()
                    price = subtree.select('.prod-price > span').text()

                    cards.append({
                        "image": image,
                        "title": title,
                        "serial": serial,
                        "price": price
                    })

                except Exception as e:
                    print(f"Не удалось получить карточку: {e}")

            return (cards, shown, total)

        except Exception as e:
            print(f"Ошибка получения страницы категории: {e}")
            return (None, None, None)
