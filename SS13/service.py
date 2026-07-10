from sqlalchemy.orm import Session
from model import MenuItem
from schemas import DishCreate, DishUpdate
from fastapi import HTTPException, status
from schemas import BaseResponse
from typing import Any
from datetime import datetime
from fastapi.responses import JSONResponse
def to_dict(dish):
    return {
        "item_id": dish.item_id,
        "dish_code": dish.dish_code,
        "dish_name": dish.dish_name,
        "calorie_count": dish.calorie_count,
        "price": dish.price,
        "status": dish.status
    }


def success_response(status_code: int, message: str, data: Any, error: str, path: str = None):
    return BaseResponse(
        status_code=status_code,
        message=message,
        data = data,
        error=error,
        timestamp=datetime.now().isoformat(),
        path= path
    )

def fail_response(status_code: int, message: str, data: Any = None, error: str = None, path: str = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code":status_code,
            "message":message,
            "data": data,
            "error":error,
            "timestamp":datetime.now().isoformat(),
            "path": path
        } 
    )


def create_dish_ser(db: Session, dish_n: DishCreate, dish_code: str):
    dish = db.query(MenuItem).filter(MenuItem.dish_code == dish_code).first()

    if dish:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dish Exists"
        )

    new_dish = MenuItem(**dish_n.model_dump(exclude_unset=True))
    try:
        db.add(new_dish)
        db.commit()
        db.refresh(new_dish)

        return new_dish
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


def get_all_menu(db: Session):
    menu = db.query(MenuItem).all()
    if not menu:
        return {
            "data": []
        }
    
    return menu

def get_dish_ser(db: Session, item_id: int):
    dish = db.query(MenuItem).filter(MenuItem.item_id == item_id).first()

    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dish Not Found"
        )

    return dish

def update_dish_ser(db: Session, item_id: int, dish: DishUpdate):
    dish_db = db.query(MenuItem).filter(MenuItem.item_id == item_id).first()
    if not dish_db:
        return None

    update_dish = dish.model_dump()

    for key, value in update_dish.items():
        setattr(dish_db, key, value)
    try:
        db.commit()
        db.refresh(dish_db)
        return dish_db
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def delete_dish_ser(db: Session, item_id: int):
    dish_db = db.query(MenuItem).filter(MenuItem.item_id == item_id).first()
    if not dish_db:
        return None

    try:
        db.delete(dish_db)
        db.commit()
        return dish_db
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    