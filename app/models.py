from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

order_items = Table(
    "order_items",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("menu_item_id", Integer, ForeignKey("menu_items.id"))
)

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    orders = relationship("Order", secondary=order_items, back_populates="items")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("MenuItem", secondary=order_items, back_populates="orders")