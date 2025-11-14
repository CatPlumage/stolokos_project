import pandas as pd
from db_init import SessionLocal
import models  # PickupPoint

session = SessionLocal()

# Загружаем Excel, header=None так как нет заголовка
pickup_file = r"C:\Users\posun\Desktop\проект по стоколос\excel\Пункты выдачи_import.xlsx"
df_pickup = pd.read_excel(pickup_file, header=None, usecols="A")  # только столбец A

try:
    for _, row in df_pickup.iterrows():
        # Преобразуем значение в строку и убираем пробелы
        full_text = str(row.iloc[0]).strip()
        if not full_text or full_text.lower() == 'nan':
            continue

        # Разбираем на части
        parts = [p.strip() for p in full_text.split(',')]
        code = parts[0] if len(parts) > 0 else None
        city = parts[1] if len(parts) > 1 else None
        street = parts[2] if len(parts) > 2 else None
        building = parts[3] if len(parts) > 3 else None
        full_address = ", ".join(parts[1:]) if len(parts) > 1 else full_text

        # Проверка на дубликаты
        pickup = session.query(models.PickupPoint).filter(
            (models.PickupPoint.code == code) | (models.PickupPoint.full_address == full_address)
        ).first()
        if pickup:
            continue

        # Создаём запись
        pickup_point = models.PickupPoint(
            code=code,
            city=city,
            street=street,
            building=building,
            full_address=full_address
        )
        session.add(pickup_point)

    session.commit()
    print("Пункты выдачи успешно импортированы!")

except Exception as e:
    session.rollback()
