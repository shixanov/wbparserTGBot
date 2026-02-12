# Search Around The Market - TG Bot

тг-бот для парсинга информации о товарах с wb

##  main functions
- **поиск товаров:** парсинг WB по ключевым словам
- **лимиты:** лимиты на день, 20 запросов в день максимум
- **История:** вся история запросов пользователей хранится в json файле
- **Асинхронность:** использовал aiogram, для высокой скорости обработки

## stack
- **язык:** Python 3.10+
- **библиотека бота:** aiogram 3.x
- **парсинг:** Playwright (Chromium)
- **окружение:** python-dotenv (безопасное хранение токенов)

## peculiarity
на данный момент в файле `services/marketplaces.py` установлено значение:
`headless=False`

**почему эт особенность?:** пока чт (`headless=True`), тк при значение "false", идет banip, тк вб просит капчу, пробуйте пару раз пройти капчу сами и выставлять значение true. p.s в скором времени пофикшу.

## how to launch

1. **скопируйте репозиторий:**
   ```bash
   git clone [https://github.com/shixanov/WB-Parser-TG-Bot.-Search-Around-The-Market-.git](https://github.com/shixanov/WB-Parser-TG-Bot.-Search-Around-The-Market-.git)
   cd WB-Parser-TG-Bot.-Search-Around-The-Market-
