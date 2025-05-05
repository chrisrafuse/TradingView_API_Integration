from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id          = Column(Integer, primary_key=True, index=True)
    ticker      = Column(String, index=True, nullable=True)
    action      = Column(String, nullable=True)       # "buy" / "sell"
    type        = Column(String, default="limit", nullable=True)
    quantity    = Column(Integer, nullable=True)
    price       = Column(Float, nullable=True)
    date        = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    status      = Column(String, default="polling", nullable=True)
    limit_price = Column(Float, default=0.0, nullable=True)
    order_id    = Column(String, nullable=True)
    asset_class = Column(String, nullable=True)       # "us_equity" / "crypto"
    filled_avg_price = Column(Float, default=0.0, nullable=True)
    filled_qty  = Column(Integer, default=0, nullable=True)

class Webhook(Base):
    __tablename__ = "webhooks"

    id       = Column(Integer, primary_key=True, index=True)
    ticker   = Column(String, index=True, nullable=True)
    action   = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    price    = Column(Float, nullable=True)
    date     = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    status   = Column(String, default="polling", nullable=True)
    limit_price = Column(Float, default=0.0, nullable=True)
    order_id = Column(String, nullable=True)
    message = Column(String, nullable=True)
  


class Attempt(Base):
    __tablename__ = "attempts"

    id          = Column(Integer, primary_key=True, index=True)
    ticker      = Column(String, index=True, nullable=True)
    action      = Column(String, nullable=True)       # "buy" / "sell"
    type        = Column(String, default="limit", nullable=True)
    quantity    = Column(Integer, nullable=True)
    price       = Column(Float, nullable=True)
    date        = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    status      = Column(String, default="polling", nullable=True)
    limit_price = Column(Float, default=0.0, nullable=True)
    order_id    = Column(String, nullable=True)
    asset_class = Column(String, nullable=True)       # "us_equity" / "crypto"
    filled_avg_price = Column(Float, default=0.0, nullable=True)
    filled_qty  = Column(Integer, default=0, nullable=True)