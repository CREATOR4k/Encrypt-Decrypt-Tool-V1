import re
from app.schemas import ReceiptItem

# Словарь ключевых слов для автоматической категоризации товаров
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Молочные продукты": ["молоко", "сыр", "творог", "кефир", "сметана", "йогурт", "масло слив"],
    "Мясо и птица": ["филе", "свинина", "говядина", "курица", "фарш", "колбаса", "сосиски", "цыпл"],
    "Овощи и фрукты": ["банан", "яблок", "томат", "огурц", "картоф", "лук", "морков", "мандарин"],
    "Хлеб и выпечка": ["хлеб", "батон", "булочк", "лаваш", "печенье", "сушки"],
    "Напитки": ["вода", "сок", "кофе", "чай", "напиток", "квас"],
    "Бытовая химия": ["порошок", "мыло", "шампунь", "гель", "бумага туал", "салфетк"],
}

def detect_category(product_name: str) -> str:
    lower_name = product_name.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in lower_name for word in keywords):
            return category
    return "Другое"

def parse_euroopt_receipt(raw_text: str) -> list[ReceiptItem]:
    items: list[ReceiptItem] = []
    # Ищем строки формата: "Название товара  1.500 x 4.20 = 6.30" или "Название товара  4.20"
    pattern = re.compile(
        r"^(?P<name>.+?)\s+(?:(?P<qty>\d+[.,]\d+)\s*[xх*]\s*(?P<price>\d+[.,]\d+)\s*=?\s*)?(?P<total>\d+[.,]\d+)$"
    )

    for line in raw_text.strip().splitlines():
        clean_line = line.strip()
        match = pattern.match(clean_line)
        if not match:
            continue

        name = match.group("name").strip(" .*:-")
        # Пропускаем итоговые служебные строки чека
        if any(skip in name.lower() for skip in ["итого", "всего", "оплата", "карта", "сдача", "ндс"]):
            continue

        total = float(match.group("total").replace(",", "."))
        qty = float(match.group("qty").replace(",", ".")) if match.group("qty") else 1.0
        price = float(match.group("price").replace(",", ".")) if match.group("price") else round(total / qty, 2)

        items.append(
            ReceiptItem(
                name=name,
                quantity=qty,
                price=price,
                total=total,
                category=detect_category(name),
            )
        )
    return items
