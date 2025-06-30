from pydantic import BaseModel
from typing import List
from datetime import datetime

class MenuItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Margherita Pizza",
                "price": 12.99,
                "is_available": True
            }
        }

class MenuItemOut(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Margherita Pizza",
                "price": 12.99,
                "is_available": True
            }
        }

class OrderCreate(BaseModel):
    customer_name: str
    item_ids: List[int]

    class Config:
        json_schema_extra = {
            "example": {
                "customer_name": "John Doe",
                "item_ids": [1, 2]
            }
        }

class OrderOut(BaseModel):
    id: int
    customer_name: str
    created_at: datetime
    items: List[MenuItemOut]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "customer_name": "John Doe",
                "created_at": "2025-06-30T17:11:00",
                "items": [
                    {
                        "id": 1,
                        "name": "Margherita Pizza",
                        "price": 12.99,
                        "is_available": True
                    }
                ]
            }
        }