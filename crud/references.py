from typing import List
from sqlalchemy.orm import Session
from database.db_init import SessionLocal
from database.models import Category, Manufacturer, Supplier, PickupPoint, OrderStatus, User

def get_all_categories(db:Session=None)->List[Category]:
    db = db or SessionLocal()
    lst = db.query(Category).all()
    db.close()
    return lst

def get_all_manufacturers(db:Session=None)->List[Manufacturer]:
    db = db or SessionLocal()
    lst = db.query(Manufacturer).all()
    db.close()
    return lst

def get_all_suppliers(db:Session=None)->List[Supplier]:
    db = db or SessionLocal()
    lst = db.query(Supplier).all()
    db.close()
    return lst

def get_all_order_statuses(db:Session=None)->List[OrderStatus]:
    db = db or SessionLocal()
    lst = db.query(OrderStatus).all()
    db.close()
    return lst

def get_all_pickup_points(db:Session=None):
    db = db or SessionLocal()
    lst = db.query(PickupPoint).all()
    db.close()
    return lst

def get_all_order_statuses(db: Session = None) -> List[OrderStatus]:
    db = db or SessionLocal()
    try:
        statuses = db.query(OrderStatus).order_by(OrderStatus.id).all()
        return statuses
    finally:
        db.close()

def get_all_pickup_points(db: Session = None) -> List[PickupPoint]:
    db = db or SessionLocal()
    try:
        points = db.query(PickupPoint).order_by(PickupPoint.city, PickupPoint.street).all()
        return points
    finally:
        db.close()

def get_all_users(db: Session = None):
    """Получить всех пользователей"""
    db = db or SessionLocal()
    try:
        users = db.query(User).order_by(User.full_name).all()
        return users
    finally:
        db.close()
