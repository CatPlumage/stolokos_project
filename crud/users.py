from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from database.db_init import SessionLocal
from database.models import User, Role
from typing import Optional, Dict


def get_user_by_id(user_id:int, db:Session = None)->Optional[User]:
    db = db or SessionLocal()
    u = db.query(User).options(joinedload(User.role)).filter(User.id==user_id).first()
    db.close()
    return u

ROLE_MAP = {
    2: "administrator",
    3: "manager",
    4: "client"
}

def get_user_by_login(login: str, db: Session = None) -> Optional[User]:
    """
    Возвращает объект User с заранее подгруженной ролью.
    Это позволяет безопасно обращаться к user.role без ошибок DetachedInstanceError.
    """
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        user = db.query(User).options(joinedload(User.role)) \
                 .filter(User.login == login).first()
        return user
    finally:
        if own_session:
            db.close()
def create_user(full_name:str, login:str, password:str, role_id:int, db:Session=None)->User:
    db = db or SessionLocal()
    user = User(full_name=full_name, login=login, password=password, role_id=role_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def get_all_roles(db:Session=None):
    db = db or SessionLocal()
    roles = db.query(Role).all()
    db.close()
    return roles
