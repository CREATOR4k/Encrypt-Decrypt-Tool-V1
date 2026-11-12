import json
import re
import requests
from bs4 import BeautifulSoup

def parse_evroopt_receipt(url: str, cookies: dict = None) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers, cookies=cookies, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    receipt_data = {
        "store": "Тут должен быть магазин",
        "url": url,
        "date": None,
        "total": 0.0,
        "items": []
    }
    
    # 1. Поиск даты (ищем стандартный формат ДД.ММ.ГГГГ ЧЧ:ММ)
    date_match = re.search(r"\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}(?::\d{2})?", soup.get_text())
    if date_match:
        receipt_data["date"] = date_match.group(0)

    # 2. Парсинг позиций (АДАПТИРУЙТЕ СЕЛЕКТОРЫ ПОД ВАШ HTML)
    # Например, если товары лежат в таблице <tr> или блоках <div class="receipt-item">
    rows = soup.select("table tr")  # Замените на реальный селектор строки товара
    
    for row in rows:
        cols = [col.get_text(strip=True) for col in row.find_all(["td", "div"]) if col.get_text(strip=True)]
        
        # Пропускаем заголовки и пустые строки (обычно в строке товара минимум название, кол-во и сумма)
        if len(cols) >= 3:
            try:
                name = cols[0]
                # Очищаем числа от пробелов и меняем запятую на точку
                quantity = float(cols[1].replace(",", ".").replace(" ", ""))
                price_total = float(cols[-1].replace(",", ".").replace(" ", ""))
                
                receipt_data["items"].append({
                    "name": name,
                    "quantity": quantity,
                    "total_price": price_total
                })
            except ValueError:
                # Строка не является товарной позицией (например, шапка таблицы)
                continue

    # 3. Подсчет или извлечение итоговой суммы
    if receipt_data["items"]:
        receipt_data["total"] = round(sum(item["total_price"] for item in receipt_data["items"]), 2)

    return receipt_data

if __name__ == "__main__":
    # Вставьте сюда реальную ссылку на чек
    RECEIPT_URL = input("URL-check: ")
    
    # Если чек открывается только после входа в личный кабинет, 
    # скопируйте Cookie из браузера (F12 -> Network -> Headers -> Cookie)
    SESSION_COOKIES = {
        # "session_id": "ваш_токен_сессии"
    }
    
    data = parse_evroopt_receipt(RECEIPT_URL, cookies=SESSION_COOKIES)
    
    # Сохраняем в файл с поддержкой кириллицы
    with open("receipt.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(json.dumps(data, ensure_ascii=False, indent=2))
