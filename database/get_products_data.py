import pandas as pd
from database.db_init import SessionLocal
from database.models import Product, Category, Manufacturer, Supplier

session = SessionLocal()

excel_file = r"E:\CatPlumage\School\PROJECT\excel\Tovar.xlsx"
df_product = pd.read_excel(excel_file)

try:
    for _, row in df_product.iterrows():
        # ---- Category ----
        category_name = row["Категория товара"]
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            session.add(category)
            session.flush()  # чтобы получить category.id

        # ---- Manufacturer ----
        manufacturer_name = row["Производитель"]
        manufacturer = session.query(Manufacturer).filter_by(name=manufacturer_name).first()
        if not manufacturer:
            manufacturer = Manufacturer(name=manufacturer_name)
            session.add(manufacturer)
            session.flush()

        # ---- Supplier ----
        supplier_name = row["Поставщик"]
        supplier = session.query(Supplier).filter_by(name=supplier_name).first()
        if not supplier:
            supplier = Supplier(name=supplier_name)
            session.add(supplier)
            session.flush()

        # ---- Product ----
        article = row["Артикул"]
        product = session.query(Product).filter_by(article=article).first()
        if product:
            print(f"Товар с артикулом {article} уже существует, пропускаем")
            continue

        product = Product(
            article=article,
            name=row["Наименование товара"],
            quantity=row.get("Кол-во на складе", 0),
            price=row.get("Цена"),
            description=row.get("Описание товара"),
            discount=row.get("Действующая скидка", 0),
            image_path=row.get("Фото"),
            category_id=category.id,
            manufacturer_id=manufacturer.id,
            supplier_id=supplier.id
        )
        session.add(product)

    session.commit()
    print("Данные успешно импортированы в products и связанные таблицы")

except Exception as e:
    session.rollback()
    print("Ошибка при импорте данных:", e)

finally:
    session.close()
