from typing import Optional, List
from sqlalchemy.orm import Session
from database.models import Order, OrderDetail
from database.db_init import SessionLocal

def get_order_by_id(order_id: int, db: Session = SessionLocal()) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def get_all_orders(db: Session = SessionLocal()) -> List[Order]:
    return db.query(Order).all()

def create_order(user_id: int, pickup_point_id: int, status_id: int,
                 delivery_date=None, pickup_code: str = "", db: Session = SessionLocal()) -> Order:
    order = Order(
        user_id=user_id,
        pickup_point_id=pickup_point_id,
        status_id=status_id,
        delivery_date=delivery_date,
        pickup_code=pickup_code
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def update_order(order_id: int, **kwargs) -> Optional[Order]:
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    for key, value in kwargs.items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

def delete_order(order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()

def create_order_detail(order_id: int, product_id: int, quantity: int, price_at_order: float,
                        db: Session = SessionLocal()) -> OrderDetail:
    detail = OrderDetail(order_id=order_id, product_id=product_id,
                         quantity=quantity, price_at_order=price_at_order)
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail
