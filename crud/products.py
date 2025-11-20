from typing import Optional, List
from sqlalchemy.orm import Session
from database.models import Product
from database.db_init import SessionLocal

def get_product_by_id(product_id: int, db: Session = SessionLocal()) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session = SessionLocal()) -> List[Product]:
    return db.query(Product).all()

def create_product(name: str, category_id: int, manufacturer_id: int, supplier_id: int,
                   price: float, quantity: int, discount: float = 0.0,
                   description: str = "", image_path: str = "", db: Session = SessionLocal()) -> Product:
    product = Product(
        name=name,
        category_id=category_id,
        manufacturer_id=manufacturer_id,
        supplier_id=supplier_id,
        price=price,
        quantity=quantity,
        discount=discount,
        description=description,
        image_path=image_path
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(product_id: int, **kwargs) -> Optional[Product]:
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    for key, value in kwargs.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        if product.order_details:
            raise Exception("Товар присутствует в заказах и не может быть удален")
        db.delete(product)
        db.commit()
