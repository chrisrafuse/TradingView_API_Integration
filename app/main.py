from fastapi import FastAPI, Depends
from app.schemas import TradingViewWebhook, OrderResponse

from app.alpaca_client import AlpacaClient
from app.config import settings
from app.routers import orders, webhooks, positions
from . import models
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
alpaca = AlpacaClient()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
app.include_router(positions.router, prefix="/api/positions", tags=["positions"])

@app.get("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    # Do NOT override valid API routes
    if full_path.startswith("api/") or full_path.startswith("assets/") or full_path.startswith("docs") or full_path.startswith("redoc"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    index_path = os.path.join("frontend", "dist", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=500, content={"detail": "Frontend not built yet"})