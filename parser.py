import requests
from lxml import html
import json
import re
import ast


class Parser:
    # Получаем HTML разметку по ссылке
    def _getcontent(self, link):
        res = requests.get(link)
        res.raise_for_status()
        with open('last-fetch.html', 'w', encoding='utf-8') as file:
            file.write(res.text)
        return res.text

    def getpages(self, category):
        try:
            content = self._getcontent(
                f"https://schneider-russia.com{category}?order=viewed&onpage=24&page=1"
            )
            tree = html.fromstring(content)
            info = tree.cssselect('.category-counter')[1].text_content().strip()

            match = re.findall(r"(\d+)", info)
            if match and len(match) == 2:
                _, total = map(int, match)
            else:
                print("Кол-во страниц не найдено")
                total = None
            
            return int(total)
        
        except Exception as e:
            print(f"Не удалось получить кол-во страниц в категории: {e}")
            return None

    # Получаем список карточек товаров по категории и странице
    def get96cards(self, category, page):
        try:
            content = self._getcontent(
                f"https://schneider-russia.com{category}?order=viewed&onpage=96&page={page}"
            )
            pattern = r"'impressions'\s*:\s*(\[[^\]]*\])"
            match = re.search(pattern, content, re.DOTALL)

            print(match)

            result = match.group(1)
            cards = ast.literal_eval(result)

            json.dump(cards, open('last-cards.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

            return cards

        except Exception as e:
            print(f"Не удалось получить JSON: {e}")
            return None