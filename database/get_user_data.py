from models import User, Role
import pandas as pd
from db_init import SessionLocal

session = SessionLocal()

df_users = pd.read_excel(r"C:\Users\posun\Desktop\проект по стоколос\excel\user_import.xlsx")

try:
    for _, row in df_users.iterrows():
        role_name = row["Роль сотрудника"]
        full_name = row["ФИО"]
        login = row["Логин"]
        password = row["Пароль"]

        # Проверяем, есть ли такая роль
        role = session.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            session.add(role)
            session.flush()  # нужно, чтобы получить role.id

        # Проверяем, есть ли такой пользователь
        user = session.query(User).filter_by(login=login).first()
        if user:
            print(f"Пользователь с логином {login} уже существует.")
            continue

        # Создаём нового пользователя
        new_user = User(
            full_name=full_name,
            login=login,
            password=password,
            role_id=role.id
        )
        session.add(new_user)

    # Сохраняем все изменения
    session.commit()
    print("Данные успешно импортированы в таблицы users и roles")

except Exception as e:
    session.rollback()
    print("Ошибка при импорте данных:", e)

finally:
    session.close()