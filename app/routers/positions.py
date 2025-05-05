from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.models import Webhook
from app.database import get_db  # you should already have this
from app.alpaca_client import AlpacaClient  # assuming you have this client set up
from typing import Optional
from app.schemas import PositionSchema
from app.order_manager import manage_order
from datetime import date



router = APIRouter()
alpaca = AlpacaClient()

@router.get("/live", response_model=List[PositionSchema])
async def get_orders_live(db: Session = Depends(get_db)):

    print("Fetching positions from the Alpaca...")

    orders = await alpaca.get_all_position()    
    if not orders:
        print("No Positions found in Alpaca.")
        return []
    print(f"Found {len(orders)} orders in Alpaca.")
    return [
        PositionSchema(
            symbol=o["symbol"],
            side=o["side"],
            qty=o["qty"],
            # price=o["filled_avg_price"],
            cost_base=str(o["cost_basis"]),
            market_value=o["market_value"],
            current_price=o["current_price"],            
        )
        for o in orders
    ]
    
    
