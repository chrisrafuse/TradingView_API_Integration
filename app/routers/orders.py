from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import OrderSchema
from app.models import Order 
from app.database import get_db  # you should already have this
from app.alpaca_client import AlpacaClient  # assuming you have this client set up


router = APIRouter()
alpaca = AlpacaClient()

@router.get("/", response_model=List[OrderSchema])
def get_orders(db: Session = Depends(get_db)):

    print("Fetching orders from the database...")
    orders = db.query(Order).all()

    print(orders)
    if not orders:
        print("No orders found in the database.")
        return []
    print(f"Found {len(orders)} orders in the database.")
    return [
        OrderSchema(
            ticker=o.ticker,
            action=o.action,
            quantity=str(o.quantity),
            price=str(o.price),
            date=str(o.date)[:10],
            status=o.status,
            limitPrice= str(o.limit_price),
        )
        for o in orders
    ]


@router.get("/live", response_model=List[OrderSchema])
async def get_orders_live(db: Session = Depends(get_db)):

    print("Fetching orders from the Alpaca...")

    orders = await alpaca.get_orders()    
    if not orders:
        print("No orders found in Alpaca.")
        return []
    print(f"Found {len(orders)} orders in Alpaca.")
    return [
        OrderSchema(
            ticker=o["symbol"],
            action=o["side"],
            quantity=o["qty"],
            # price=o["filled_avg_price"],
            date=str(o["created_at"])[:19],
            status=o["status"],
            limitPrice=o["limit_price"],
            type=o["type"],
            position_intent=o["position_intent"],
        )
        for o in orders
    ]
    
    
