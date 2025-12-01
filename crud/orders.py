from typing import Optional, List
from sqlalchemy.orm import Session
from database.db_init import SessionLocal
from database.models import Order, OrderDetail

def get_order_by_id(order_id:int, db:Session=None)->Optional[Order]:
    db = db or SessionLocal()
    o = db.query(Order).filter(Order.id==order_id).first()
    db.close()
    return o

def get_all_orders(db:Session=None)->List[Order]:
    db = db or SessionLocal()
    lst = db.query(Order).all()
    db.close()
    return lst

def create_order(user_id:int, pickup_point_id:int=None, status_id:int=None,
                 delivery_date=None, pickup_code:str=None, db:Session=None)->Order:
    db = db or SessionLocal()
    o = Order(user_id=user_id, pickup_point_id=pickup_point_id, status_id=status_id,
              delivery_date=delivery_date, pickup_code=pickup_code)
    db.add(o)
    db.commit()
    db.refresh(o)
    db.close()
    return o

def update_order(order_id:int, db:Session=None, **kwargs)->Optional[Order]:
    db = db or SessionLocal()
    o = db.query(Order).filter(Order.id==order_id).first()
    if not o:
        db.close()
        return None
    for k,v in kwargs.items():
        if hasattr(o, k):
            setattr(o, k, v)
    db.commit()
    db.refresh(o)
    db.close()
    return o

def delete_order(order_id:int, db:Session=None):
    db = db or SessionLocal()
    o = db.query(Order).filter(Order.id==order_id).first()
    if not o:
        db.close()
        return
    db.delete(o)
    db.commit()
    db.close()

def create_order_detail(order_id:int, product_id:int, quantity:int, price_at_order:float, db:Session=None)->OrderDetail:
    db = db or SessionLocal()
    d = OrderDetail(order_id=order_id, product_id=product_id, quantity=quantity, price_at_order=price_at_order)
    db.add(d)
    db.commit()
    db.refresh(d)
    db.close()
    return d
