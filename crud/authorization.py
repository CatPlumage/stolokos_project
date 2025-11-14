from database.models import User
from database.db_init import SessionLocal

session = SessionLocal()

def get_user_by_login(login):
    if login:
        user = session.query(User).filter(User.login == login).first()
        return user
    else:
        return None