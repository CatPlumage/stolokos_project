# ui_products.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt


class ProductsWindow(QWidget):
    def __init__(self, role: str):
        super().__init__()

        self.role = role          # guest | client | manager | admin
        self.setWindowTitle("Товары")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Заголовок
        self.title = QLabel(f"Окно товаров (роль: {self.role})")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        # Панель фильтрации (только менеджер и админ)
        self.filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию...")

        self.sort_box = QComboBox()
        self.sort_box.addItems(["Без сортировки", "Цена ↑", "Цена ↓"])

        self.filter_layout.addWidget(self.search_input)
        self.filter_layout.addWidget(self.sort_box)

        if self.role in ("manager", "admin"):
            self.layout.addLayout(self.filter_layout)

        # Таблица товаров
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Цена"])
        self.layout.addWidget(self.table)

        # Кнопки управления
        self.buttons_layout = QHBoxLayout()

        self.btn_add = QPushButton("Добавить товар")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить товар")
        self.btn_orders = QPushButton("Заказы")

        # Добавляем кнопки в слой
        self.buttons_layout.addWidget(self.btn_orders)
        self.buttons_layout.addWidget(self.btn_add)
        self.buttons_layout.addWidget(self.btn_edit)
        self.buttons_layout.addWidget(self.btn_delete)

        # Доступ к функционалу по ролям
        if self.role == "client":
            self.btn_add.hide()
            self.btn_edit.hide()
            self.btn_delete.hide()
            self.btn_orders.hide()

        if self.role == "manager":
            self.btn_add.hide()
            self.btn_edit.hide()
            self.btn_delete.hide()
            # может просматривать заказы
            # кнопка отображается

        if self.role == "admin":
            # полный доступ → ничего не скрываем
            pass

        if self.role == "guest":
            # только просмотр
            self.btn_add.hide()
            self.btn_edit.hide()
            self.btn_delete.hide()
            self.btn_orders.hide()

        self.layout.addLayout(self.buttons_layout)

        # Заполняем тестовыми товарами
        self.load_products()

    def load_products(self):
        """Заглушка для отображения списка товаров."""
        products = [
            (1, "Ноутбук", 55000),
            (2, "Монитор", 12000),
            (3, "Клавиатура", 3000)
        ]

        self.table.setRowCount(len(products))

        for row, (pid, name, price) in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(str(price)))
