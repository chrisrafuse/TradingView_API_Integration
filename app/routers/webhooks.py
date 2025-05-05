from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.models import Webhook
from app.database import get_db  # you should already have this
from app.alpaca_client import AlpacaClient  # assuming you have this client set up
from typing import Optional
from app.schemas import TradingViewWebhook, OrderResponse, WebhookSchema
from app.order_manager import manage_order
from datetime import date



router = APIRouter()
alpaca = AlpacaClient()

@router.get("/db", response_model=List[WebhookSchema])
def get_webhooks(db: Session = Depends(get_db)):

    print("Fetching orders from the database...")
    orders = db.query(Webhook).all()
    if not orders:
        print("No orders found in the database.")
        return []
    print(f"Found {len(orders)} orders in the database.")
    result =  [
        WebhookSchema(
            ticker=o.ticker,
            action=o.action,
            quantity=str(o.quantity),
            price=str(o.price),
            date=str(o.date)[:19],   
            status=o.status,
            limitPrice=str(o.limit_price),
            order_id=o.order_id,
            message=o.message
        )
        for o in orders
    ]
    return result
    



@router.post("/db", response_model=OrderResponse)
async def webhook_handler(
    payload: TradingViewWebhook, db: Session = Depends(get_db)
):    
    print("Webhook Detected")
    print(payload)
    order = await manage_order(
        symbol=payload.ticker,
        action=payload.action,
        quantity=1,
        price=payload.price,
        db=db,
    )
    # print(order)
    return OrderResponse(order_id=order["id"], status=order["status"])


