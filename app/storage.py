from collections import defaultdict
from datetime import datetime
from app.schemas import CategoryStat, ReceiptItem, ReceiptResponse

receipts_db: list[ReceiptResponse] = []
next_id = 1

def save_receipt(store_address: str, items: list[ReceiptItem]) -> ReceiptResponse:
    global next_id
    total_sum = round(sum(item.total for item in items), 2)
    receipt = ReceiptResponse(
        id=next_id,
        created_at=datetime.now(),
        store_address=store_address,
        items=items,
        total_sum=total_sum,
    )
    receipts_db.append(receipt)
    next_id += 1
    return receipt

def get_all_receipts() -> list[ReceiptResponse]:
    return receipts_db

def get_stats_by_category() -> list[CategoryStat]:
    totals: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)

    for receipt in receipts_db:
        for item in receipt.items:
            totals[item.category] += item.total
            counts[item.category] += 1

    return [
        CategoryStat(
            category=cat,
            total_spent=round(amount, 2),
            items_count=counts[cat],
        )
        for cat, amount in sorted(totals.items(), key=lambda x: x[1], reverse=True)
    ]
