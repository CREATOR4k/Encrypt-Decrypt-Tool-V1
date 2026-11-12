from datetime import datetime
from pydantic import BaseModel, Field

class ReceiptItem(BaseModel):
    name: str
    quantity: float = 1.0
    price: float
    total: float
    category: str = "Другое"

class ReceiptRawInput(BaseModel):
    store_address: str = Field(default="Евроопт, Могилев", description="Адрес магазина")
    raw_text: str = Field(..., description="Скопированный текст чека из Еплюс или фото")

class ReceiptResponse(BaseModel):
    id: int
    created_at: datetime
    store_address: str
    items: list[ReceiptItem]
    total_sum: float

class CategoryStat(BaseModel):
    category: str
    total_spent: float
    items_count: int
