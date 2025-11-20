import os
from PyQt6 import QtWidgets, QtGui, QtCore
from crud.products import get_all_products
from crud.references import get_all_categories, get_all_suppliers


def get_image_path(filename: str | None):
    """
    Возвращает абсолютный путь к изображению в папке images.
    Если файла нет — возвращает None.
    """
    if not filename:
        return None

    # Путь к текущей папке (user_interface)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Папка проекта
    project_dir = os.path.dirname(base_dir)

    # Путь к папке images
    img_path = os.path.join(project_dir, "images", filename)

    return img_path


class ProductsWindow(QtWidgets.QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.setWindowTitle("Список товаров")
        self.setMinimumSize(900, 600)
        self.setWindowIcon(QtGui.QIcon("resources/logo.png"))

        # --- Приветствие пользователя --- #
        self.label_user = QtWidgets.QLabel(self)
        self.label_user.move(700, 10)
        self.label_user.setFixedWidth(200)
        if user:
            self.label_user.setText(f"{user.full_name} ({user.role.name})")
        else:
            self.label_user.setText("Гость")

        # --- Таблица товаров --- #
        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(20, 50, 850, 500)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Наименование", "Категория", "Производитель",
            "Поставщик", "Цена", "Количество", "Скидка",
            "Описание", "Фото"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Загружаем товары
        self.load_products()

    def load_products(self):
        products = get_all_products()
        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            # --- Заполнение текстовых колонок --- #
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(product.id)))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(product.name))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(product.category.name if product.category else ""))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(product.manufacturer.name if product.manufacturer else ""))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(product.supplier.name if product.supplier else ""))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(product.price)))
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(product.quantity)))
            self.table.setItem(row, 7, QtWidgets.QTableWidgetItem(f"{product.discount}%"))
            self.table.setItem(row, 8, QtWidgets.QTableWidgetItem(product.description or ""))

            # --- Фото товара --- #
            label = QtWidgets.QLabel()
            label.setFixedSize(80, 50)

            # Получаем путь к изображению
            img_path = get_image_path(product.image_path)

            # Загружаем изображение
            pixmap = QtGui.QPixmap(img_path) if img_path else QtGui.QPixmap("resources/picture.png")

            # Если путь неверный — подставляем картинку по умолчанию
            if pixmap.isNull():
                pixmap = QtGui.QPixmap("resources/picture.png")

            pixmap = pixmap.scaled(label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            label.setPixmap(pixmap)

            self.table.setCellWidget(row, 9, label)

            # --- Подсветка строк --- #

            # Большая скидка
            if product.discount and float(product.discount) > 15:
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QtGui.QColor("#2E8B57"))

            # Нет в наличии
            if product.quantity == 0:
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QtGui.QColor("#ADD8E6"))
