# ui/ui_order_edit.py
from PyQt6 import QtWidgets, QtCore

class Ui_OrderEditWindow:
    def setupUi(self, Dialog):
        BG_DEFAULT = "#FFFFFF"
        BG_SECONDARY = "#7FFF00"
        BG_ACCENT = "#00FA9A"
        TEXT_DARK = "#000000"

        Dialog.setWindowTitle("Добавить / Редактировать заказ")
        Dialog.resize(800, 600)
        Dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
            QLabel {{
                color: {TEXT_DARK};
                font-family: "Times New Roman";
            }}
            QLineEdit, QComboBox, QDateEdit {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 2px 4px;
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
            QPushButton {{
                background-color: {BG_SECONDARY};
                color: {TEXT_DARK};
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-family: "Times New Roman";
                font-size: 9pt;
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {BG_ACCENT};
            }}
            QTableWidget {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                gridline-color: #DDDDDD;
                border: 1px solid #CCCCCC;
                font-family: "Times New Roman";
                font-size: 9pt;
            }}
            QHeaderView::section {{
                background-color: #F0F0F0;
                color: {TEXT_DARK};
                padding: 4px;
                border: 1px solid #DDDDDD;
                font-weight: bold;
            }}
            /* Стиль для QMessageBox */
            QMessageBox {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
            QMessageBox QLabel {{
                color: {TEXT_DARK};
            }}
            QMessageBox QPushButton {{
                background-color: {BG_SECONDARY};
                color: {TEXT_DARK};
                border: none;
                border-radius: 5px;
                padding: 4px 10px;
                font-weight: bold;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {BG_ACCENT};
            }}
        """)

        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        
        # Форма с основными данными заказа
        self.formLayout = QtWidgets.QFormLayout()
        
        self.cmb_user = QtWidgets.QComboBox()
        self.cmb_status = QtWidgets.QComboBox()
        self.cmb_pickup_point = QtWidgets.QComboBox()
        
        self.date_order = QtWidgets.QDateEdit()
        self.date_order.setCalendarPopup(True)
        self.date_order.setDate(QtCore.QDate.currentDate())
        
        self.date_delivery = QtWidgets.QDateEdit()
        self.date_delivery.setCalendarPopup(True)
        self.date_delivery.setDate(QtCore.QDate.currentDate().addDays(3))
        
        self.input_pickup_code = QtWidgets.QLineEdit()
        
        self.formLayout.addRow("Пользователь:", self.cmb_user)
        self.formLayout.addRow("Статус:", self.cmb_status)
        self.formLayout.addRow("Пункт выдачи:", self.cmb_pickup_point)
        self.formLayout.addRow("Дата заказа:", self.date_order)
        self.formLayout.addRow("Дата доставки:", self.date_delivery)
        self.formLayout.addRow("Код получения:", self.input_pickup_code)
        
        self.verticalLayout.addLayout(self.formLayout)
        
        # Разделитель
        self.verticalLayout.addWidget(QtWidgets.QLabel("Товары в заказе:"))
        
        # Таблица товаров в заказе
        self.table_products = QtWidgets.QTableWidget()
        self.table_products.setColumnCount(4)
        self.table_products.setHorizontalHeaderLabels(["Товар", "Количество", "Цена", "Сумма"])
        self.table_products.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_products.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.table_products)
        
        # Панель добавления товаров
        self.add_product_layout = QtWidgets.QHBoxLayout()
        
        self.cmb_product = QtWidgets.QComboBox()
        self.cmb_product.setMinimumWidth(300)
        
        self.label_price = QtWidgets.QLabel("Цена: -")
        
        self.input_quantity = QtWidgets.QSpinBox()
        self.input_quantity.setMinimum(1)
        self.input_quantity.setMaximum(999)
        self.input_quantity.setValue(1)
        
        self.btn_add_product = QtWidgets.QPushButton("Добавить")
        self.btn_remove_product = QtWidgets.QPushButton("Удалить")
        
        self.add_product_layout.addWidget(QtWidgets.QLabel("Товар:"))
        self.add_product_layout.addWidget(self.cmb_product)
        self.add_product_layout.addWidget(self.label_price)
        self.add_product_layout.addWidget(QtWidgets.QLabel("Кол-во:"))
        self.add_product_layout.addWidget(self.input_quantity)
        self.add_product_layout.addWidget(self.btn_add_product)
        self.add_product_layout.addWidget(self.btn_remove_product)
        
        self.verticalLayout.addLayout(self.add_product_layout)
        
        # Общая сумма
        self.label_total = QtWidgets.QLabel("Общая сумма: 0.00 руб.")
        self.label_total.setStyleSheet("font-weight: bold; font-size: 11pt;")
        self.verticalLayout.addWidget(self.label_total)
        
        # Кнопки сохранения/отмены
        self.btns_layout = QtWidgets.QHBoxLayout()
        self.btn_save = QtWidgets.QPushButton("Сохранить")
        self.btn_cancel = QtWidgets.QPushButton("Отмена")
        
        self.btns_layout.addWidget(self.btn_save)
        self.btns_layout.addWidget(self.btn_cancel)
        self.btns_layout.addStretch()
        
        self.verticalLayout.addLayout(self.btns_layout)