from typing import Optional
from sqlalchemy.orm import Session
from database.models import User, Role
from database.db_init import SessionLocal

# --- Пользователи --- #

def get_user_by_id(user_id: int, db: Session = SessionLocal()) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_login(login: str, db: Session = SessionLocal()) -> Optional[User]:
    return db.query(User).filter(User.login == login).first()

def create_user(full_name: str, login: str, password: str, role_id: int, db: Session = SessionLocal()) -> User:
    user = User(full_name=full_name, login=login, password=password, role_id=role_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(user_id: int, **kwargs) -> Optional[User]:
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

# --- Роли --- #

def get_role_by_name(name: str, db: Session = SessionLocal()) -> Optional[Role]:
    return db.query(Role).filter(Role.name == name).first()

def get_all_roles(db: Session = SessionLocal()):
    return db.query(Role).all()
