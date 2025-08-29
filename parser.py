import requests
from lxml import html


class Parser():
    def __init__(self):
        pass

    # Получаем HTML разметку по ссылке
    def get(self, link):
        res = requests.get(link)
        res.raise_for_status()
        return res.text
    
    # Безопастный cssselect
    def select(self, tree, selector, default='', attr=None):
        try:
            if not attr:
                return tree.cssselect(selector)[0].text_content().strip()
            else:
                return tree.cssselect(selector)[0].get(attr)
        except:
            return default

    # Получаем доп.информации о категории
    def get_category_info(self, tree):
        try:
            cat_cards_count = tree.cssselect('.category-counter')[0].text_content().strip()
            cat_cards_count = cat_cards_count.split(' ')[0]

            is_full_parsed = tree.cssselect('.category-counter')[1].text_content().strip()
            is_full_parsed = (is_full_parsed.count(cat_cards_count) == 2)

            return (cat_cards_count, is_full_parsed)

        except Exception as e:
            print(f"Ошибка получения доп.информации о категории: {e}")
            return (0, False)

    # Получаем список карточек товаров по категории и странице
    def get_cards(self, category, page):
        # try:
            content = self.get(f"https://schneider-russia.com{category}?order=viewed&onpage=96&page={page}")
            tree = html.fromstring(content)

            cat_cards_count, is_full_parsed = self.get_category_info(tree)

            cards = tree.cssselect('.grid-products > li')
            if not cards:
                print("Карточки не найдены")

            cards_list = []
            for card in cards:
                # try:
                    image = self.select(card, '.category-item-image > img', '', 'src')
                    title = self.select(card, '.category-item-title')
                    serial = self.select(card, '.category-item-brand')
                    price = self.select(card, '.prod-price > span')

                    cards_list.append({
                        "image": image,
                        "title": title,
                        "serial": serial,
                        "price": price
                    })

                # except Exception as e:
                #     print(f"Не удалось получить карточку: {e}")
                #     continue
            
            return (cards_list, int(cat_cards_count)//96, is_full_parsed)

        # except Exception as e:
        #     print(f"Ошибка получения страницы: {e}")
        #     return (None, None, None)