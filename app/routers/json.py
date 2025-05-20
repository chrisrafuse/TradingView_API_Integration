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

@router.get("/meta")
async def getJson():

    print("Fetching positions from the Alpaca...")

    return {
        "name": "Hello"
    }
    
    
