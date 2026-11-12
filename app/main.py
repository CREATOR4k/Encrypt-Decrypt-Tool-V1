from fastapi import FastAPI
from app.router import router as receipts_router

app = FastAPI(
    title="EuroCheck API",
    description="Учет расходов и аналитика по чекам Евроопта (BYN)",
    version="0.1.0",
)

app.include_router(receipts_router)
