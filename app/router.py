from fastapi import APIRouter, HTTPException, status
from app import parser, storage
from app.schemas import CategoryStat, ReceiptRawInput, ReceiptResponse

router = APIRouter(prefix="/receipts", tags=["Receipts"])

@router.post("/parse", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
def upload_and_parse_receipt(payload: ReceiptRawInput):
    items = parser.parse_euroopt_receipt(payload.raw_text)
    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось распознать товары в тексте чека",
        )
    return storage.save_receipt(payload.store_address, items)

@router.get("/", response_model=list[ReceiptResponse])
def list_receipts():
    return storage.get_all_receipts()

@router.get("/stats/categories", response_model=list[CategoryStat])
def category_statistics():
    return storage.get_stats_by_category()
