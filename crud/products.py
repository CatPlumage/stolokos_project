from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from database.db_init import SessionLocal
from database.models import Product

def get_product_by_id(product_id:int, db:Session=None)->Optional[Product]:
    db = db or SessionLocal()
    p = db.query(Product).filter(Product.id==product_id).first()
    db.close()
    return p

def get_all_products(db: Session = None):
    db = db or SessionLocal()
    try:
        products = db.query(Product)\
            .options(
                joinedload(Product.category),
                joinedload(Product.supplier),
                joinedload(Product.manufacturer)
            ).all()
        return products
    finally:
        db.close()

def create_product(name:str, category_id:int=None, manufacturer_id:int=None, supplier_id:int=None,
                   price:float=0.0, quantity:int=0, discount:float=0.0, description:str="", image_path:str=None,
                   db:Session=None)->Product:
    db = db or SessionLocal()
    p = Product(name=name, category_id=category_id, manufacturer_id=manufacturer_id,
                supplier_id=supplier_id, price=price, quantity=quantity,
                discount=discount, description=description, image_path=image_path)
    db.add(p)
    db.commit()
    db.refresh(p)
    db.close()
    return p

def update_product(product_id:int, db:Session=None, **kwargs)->Optional[Product]:
    db = db or SessionLocal()
    p = db.query(Product).filter(Product.id==product_id).first()
    if not p:
        db.close()
        return None
    for k,v in kwargs.items():
        if hasattr(p, k):
            setattr(p, k, v)
    db.commit()
    db.refresh(p)
    db.close()
    return p

def delete_product(product_id:int, db:Session=None):
    db = db or SessionLocal()
    p = db.query(Product).filter(Product.id==product_id).first()
    if not p:
        db.close()
        return
    # проверить связи с заказами
    if p.order_details and len(p.order_details) > 0:
        db.close()
        raise Exception("Товар присутствует в заказах и не может быть удалён")
    db.delete(p)
    db.commit()
    db.close()
