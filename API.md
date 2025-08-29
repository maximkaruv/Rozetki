# Парсинг постранично подкатегории

`https://schneider-russia.com/rozetki/elektricheskie-rozetki?order=viewed&onpage=96&page=2`
`/rozetki/elektricheskie-rozetki` - категория
`page=2` - страница

Кол-во товаров:
`.category-counter`[0] -> `1127 товаров`

Кол-во пройденных товаров:
`.category-counter`[0] -> `Показано 1127 из 1127`

## Карточки[]:

`.grid-products > li`

Шапка:
`.category-item-image > img`(src)

Название:
`.category-item-title`

Серия:
`.category-item-brand`

Цена:
`.price-new` -> `379 ₽`
