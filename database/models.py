from typing import List, Optional
from datetime import date
from decimal import Decimal
from sqlalchemy import String, Text, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db_init import Base


# --- Роли и пользователи ---

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("roles.id"))
    role: Mapped[Optional[Role]] = relationship(back_populates="users")

    orders: Mapped[List["Order"]] = relationship(back_populates="user")


# --- Категории, производители, поставщики ---

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="category")


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="manufacturer")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="supplier")


# --- Товары ---

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    article: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    manufacturer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("manufacturers.id"))
    supplier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("suppliers.id"))
    price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    quantity: Mapped[Optional[int]] = mapped_column(Integer)
    discount: Mapped[float] = mapped_column(Numeric(5, 2), default=0)
    image_path: Mapped[Optional[str]] = mapped_column(String(255))

    category: Mapped[Optional[Category]] = relationship(back_populates="products")
    manufacturer: Mapped[Optional[Manufacturer]] = relationship(back_populates="products")
    supplier: Mapped[Optional[Supplier]] = relationship(back_populates="products")

    order_details: Mapped[List["OrderDetail"]] = relationship(back_populates="product")


# --- Статусы заказов, пункты выдачи ---

class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    orders: Mapped[List["Order"]] = relationship(back_populates="status")


class PickupPoint(Base):
    __tablename__ = "pickup_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[Optional[str]] = mapped_column(String(20), unique=True)   
    city: Mapped[str] = mapped_column(String(100), nullable=False)         
    street: Mapped[str] = mapped_column(String(100), nullable=False)      
    building: Mapped[str] = mapped_column(String(20), nullable=False)      
    full_address: Mapped[str] = mapped_column(String(255), nullable=False) 

    orders: Mapped[List["Order"]] = relationship(back_populates="pickup_point")


# --- Заказы и детали заказов ---

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    order_date: Mapped[date] = mapped_column(Date, default=date.today)
    delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    pickup_point_id: Mapped[Optional[int]] = mapped_column(ForeignKey("pickup_points.id"))
    status_id: Mapped[Optional[int]] = mapped_column(ForeignKey("order_statuses.id"))
    pickup_code: Mapped[Optional[str]] = mapped_column(String(10))

    user: Mapped[Optional[User]] = relationship(back_populates="orders")
    pickup_point: Mapped[Optional[PickupPoint]] = relationship(back_populates="orders")
    status: Mapped[Optional[OrderStatus]] = relationship(back_populates="orders")

    details: Mapped[List["OrderDetail"]] = relationship(back_populates="order", cascade="all, delete")


class OrderDetail(Base):
    __tablename__ = "order_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_order: Mapped[float] = mapped_column(Numeric(10, 2))

    order: Mapped["Order"] = relationship(back_populates="details")
    product: Mapped["Product"] = relationship(back_populates="order_details")

    