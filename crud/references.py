from typing import List
from sqlalchemy.orm import Session
from database.models import Category, Manufacturer, Supplier, PickupPoint, OrderStatus
from database.db_init import SessionLocal

# --- Категории --- #
def get_all_categories(db: Session = SessionLocal()) -> List[Category]:
    return db.query(Category).all()

# --- Производители --- #
def get_all_manufacturers(db: Session = SessionLocal()) -> List[Manufacturer]:
    return db.query(Manufacturer).all()

# --- Поставщики --- #
def get_all_suppliers(db: Session = SessionLocal()) -> List[Supplier]:
    return db.query(Supplier).all()

# --- Пункты выдачи --- #
def get_all_pickup_points(db: Session = SessionLocal()) -> List[PickupPoint]:
    return db.query(PickupPoint).all()

# --- Статусы заказов --- #
def get_all_order_statuses(db: Session = SessionLocal()) -> List[OrderStatus]:
    return db.query(OrderStatus).all()
