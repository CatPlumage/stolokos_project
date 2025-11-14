import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from models import Product, PickupPoint, Order, OrderDetail, User
from db_init import SessionLocal

def parse_date_safe(date_str):
    """Безопасное преобразование даты из Excel."""
    try:
        return pd.to_datetime(date_str, errors='raise', dayfirst=True).date()
    except Exception:
        print(f"⚠️ Ошибка преобразования даты: {date_str}")
        return None

def parse_products_cell(cell_value):
    """
    Преобразует строку вроде 'A112T4, 2, F635R4, 2' → [('A112T4', 2), ('F635R4', 2)]
    """
    if pd.isna(cell_value):
        return []

    parts = [p.strip() for p in str(cell_value).split(',')]
    products = []
    for i in range(0, len(parts) - 1, 2):
        try:
            article = parts[i]
            quantity = int(parts[i + 1])
            products.append((article, quantity))
        except (ValueError, IndexError):
            print(f"⚠️ Ошибка парсинга артикула: {cell_value}")
            continue
    return products

def import_orders_from_excel(file_path):
    df = pd.read_excel(file_path)
    session = SessionLocal()

    try:
        for index, row in df.iterrows():
            order_number = str(row["Номер заказа"]).strip()
            order_date = parse_date_safe(row["Дата заказа"])
            delivery_date = parse_date_safe(row["Дата доставки"])
            pickup_address = str(row["Адрес пункта выдачи"]).strip()
            client_name = str(row["ФИО авторизированного клиента"]).strip()
            pickup_code = str(row["Код для получения"]).strip()

            # Найдём пункт выдачи
            pickup_point = session.query(PickupPoint).filter_by(id=pickup_address).first()
            if not pickup_point:
                print(f"⚠️ Пункт выдачи '{pickup_address}' не найден — заказ пропущен.")
                continue
            user = session.query(User).filter_by(full_name=client_name).first()
            if not user:
                print(f"⚠️ Пользователь '{client_name}' не найден — заказ пропущен.")
                continue

            # Создаём заказ
            order = Order(
                id=order_number,
                order_date=order_date,
                delivery_date=delivery_date,
                pickup_point_id=pickup_point.id,
                user=user,
                pickup_code=pickup_code
            )
            session.add(order)
            session.flush()  # Чтобы получить order.id

            # Парсим товары
            product_entries = parse_products_cell(row["Артикул заказа"])
            if not product_entries:
                print(f"⚠️ В заказе №{order_number} нет корректных товаров.")
                continue

            for article, quantity in product_entries:
                product = session.query(Product).filter_by(article=article).first()
                if not product:
                    print(f"⚠️ Товар с артикулом '{article}' не найден — пропущен.")
                    continue

                order_item = OrderDetail(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity
                )
                session.add(order_item)

        session.commit()
        print("✅ Все заказы успешно импортированы!")
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка при импорте данных: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    import_orders_from_excel(r"C:\Users\posun\Desktop\проект по стоколос\excel\Заказ_import.xlsx")
