from pydantic import BaseModel
from typing import Optional


class TradingViewWebhook(BaseModel):
    ticker: Optional[str] = None
    action: Optional[str] = None  # "buy" or "sell"
    quantity: Optional[float] = None
    price: Optional[float] = None  # limit price
    sentiment: Optional[str] = None  # "bullish" or "bearish"
    optionType: Optional[str] = None  # "call" or "put"

class OrderResponse(BaseModel):
    order_id: str
    status: str

class OrderSchema(BaseModel):
    ticker: Optional[str] = None
    action: Optional[str] = None
    quantity: Optional[str] = None
    price: Optional[str] = None
    date: Optional[str] = None
    status: Optional[str] = None
    limitPrice: Optional[str] = None
    type: Optional[str] = None
    position_intent: Optional[str] = None

    class Config:
        orm_mode = True

class WebhookSchema(BaseModel):
    ticker: Optional[str] = None
    action: Optional[str] = None
    quantity: Optional[str] = None
    price: Optional[str] = None
    date: Optional[str] = None
    status: Optional[str] = None
    limitPrice: Optional[str] = None
    order_id: Optional[str] = None
    message: Optional[str] = None

    class Config:
        orm_mode = True


class PositionSchema(BaseModel):
    symbol: Optional[str] = None
    side: Optional[str] = None
    qty: Optional[str] = None
    cost_basis: Optional[str] = None
    market_value: Optional[str] = None
    current_price: Optional[str] = None    

    class Config:
        orm_mode = True