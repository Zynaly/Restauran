from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from datetime import datetime, date
from sqlalchemy.sql import func
import os

router = APIRouter()

@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    items = db.query(models.MenuItem).filter(
        models.MenuItem.id.in_(order.item_ids),
        models.MenuItem.is_available == True
    ).all()
    if len(items) != len(order.item_ids):
        raise HTTPException(status_code=400, detail="Some items are not available or don't exist")
    db_order = models.Order(customer_name=order.customer_name)
    db_order.items = items
    db.add(db_order)
    db.commit()
    db.refresh(db_order) 
    total_price = sum(item.price for item in db_order.items) 
    timestamp = db_order.created_at.strftime("%Y-%m-%d %H:%M:%S")
    item_ids_str = ",".join(str(id) for id in order.item_ids)
    log_entry = f"{timestamp} | {db_order.customer_name} | {item_ids_str} | {total_price}\n"
    with open("orders_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry) 
    return {
        "id": db_order.id,
        "customer_name": db_order.customer_name,
        "created_at": db_order.created_at,
        "items": db_order.items,
        "total_price": total_price
    }

@router.get("/", response_model=List[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return [
        {
            "id": order.id,
            "customer_name": order.customer_name,
            "created_at": order.created_at,
            "items": order.items,
            "total_price": sum(item.price for item in order.items)
        }
        for order in orders
    ]

@router.get("/today/", response_model=List[schemas.OrderOut])
def get_todays_orders(db: Session = Depends(get_db)):
    today = date.today()
    orders = db.query(models.Order).filter(func.date(models.Order.created_at) == today).all()
    return [
        {
            "id": order.id,
            "customer_name": order.customer_name,
            "created_at": order.created_at,
            "items": order.items,
            "total_price": sum(item.price for item in order.items)
        }
        for order in orders
    ]

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "created_at": order.created_at,
        "items": order.items,
        "total_price": sum(item.price for item in order.items)
    }