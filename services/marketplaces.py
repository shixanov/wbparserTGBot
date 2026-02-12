import asyncio
from playwright.async_api import async_playwright

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

async def parse_wb(query):
    search_url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, 
            args=["--disable-blink-features=AutomationControlled"] 
        )
        context = await browser.new_context(
            user_agent=USER_AGENT,
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        try:
            await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
            
            try:
                await page.wait_for_selector("article", timeout=15000)
            except:
                print("⚠️ Товары не найдены. Скорее всего, на экране капча! Решите её вручную.")
                await asyncio.sleep(15)
            
            items = []
            cards = await page.locator("article").all()
            
            for card in cards[:5]:
                try:
                    text_content = await card.inner_text()
                    lines = text_content.split('\n')
                    
                    price = "Цена не найдена"
                    name = "Название не найдено"
                    
                    for line in lines:
                        if "₽" in line:
                            price = line.strip()
                            break
                    
                    link_locator = card.locator("a").first
                    raw_link = await link_locator.get_attribute("href")
                    full_link = raw_link if raw_link.startswith("http") else f"https://www.wildberries.ru{raw_link}"
                    
                    name_attempt = await link_locator.get_attribute("aria-label")
                    if name_attempt:
                        name = name_attempt
                    else:

                        if len(lines) > 1: name = lines[1]

                    items.append({
                        "item": name,
                        "price": price,
                        "url": full_link,
                        "marketplace": "Wildberries"
                    })
                except Exception as e:
                    continue
            
            return items
            
        except Exception as e:
            print(f"WB Parsing Error: {e}")
            return []
        finally:
            await browser.close()

async def search_all_marketplaces(query: str):
    return await parse_wb(query)