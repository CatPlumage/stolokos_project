# ui_products.py
from PyQt6 import QtWidgets, QtGui, QtCore

class Ui_ProductsWindow:
    def setupUi(self, MainWindow):
        BG_DEFAULT = "#FFFFFF"
        BG_SECONDARY = "#7FFF00"
        BG_ACCENT = "#00FA9A"
        TEXT_DARK = "#000000"

        MainWindow.setWindowTitle("Каталог товаров — Stokolos")
        MainWindow.resize(1000, 700)
        MainWindow.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                font-family: "Times New Roman";
                font-size: 9pt;
            }}
            QLabel {{
                color: {TEXT_DARK};
                font-family: "Times New Roman";
                font-size: 9pt;
            }}
            QLineEdit {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 2px 6px;
                font-family: "Times New Roman";
                font-size: 9pt;
            }}
            QLineEdit:focus {{
                border: 1px solid #000000;
            }}
            QComboBox {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 2px 6px;
                font-family: "Times New Roman";
                font-size: 9pt;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                selection-background-color: {BG_ACCENT};
                selection-color: {TEXT_DARK};
                border: 1px solid #CCCCCC;
                font-family: "Times New Roman";
                font-size: 9pt;
            }}
            QTableWidget {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                gridline-color: #DDDDDD;
                alternate-background-color: #F8F8F8;
                border: 1px solid #CCCCCC;
                selection-background-color: {BG_ACCENT};
                selection-color: {TEXT_DARK};
                font-family: "Times New Roman";
                font-size: 8pt;
            }}
            QHeaderView::section {{
                background-color: #F0F0F0;
                color: {TEXT_DARK};
                padding: 6px;
                border: 1px solid #DDDDDD;
                font-weight: bold;
                font-family: "Times New Roman";
                font-size: 8pt;
            }}
            QTableWidget::item {{
                padding: 4px;
            }}
            QPushButton {{
                background-color: {BG_SECONDARY};
                color: {TEXT_DARK};
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-family: "Times New Roman";
                font-size: 9pt;
            }}
            QPushButton:hover {{
                background-color: {BG_ACCENT};
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

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.label_user = QtWidgets.QLabel("Гость", self.centralwidget)
        self.label_user.setGeometry(650, 10, 400, 25)

        self.btn_back = QtWidgets.QPushButton("Назад", self.centralwidget)
        self.btn_back.setGeometry(10, 10, 70, 25)

        self.search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_input.setGeometry(20, 40, 300, 28)
        self.search_input.setPlaceholderText("Поиск... (название, описание, производитель...)")

        self.supplier_filter = QtWidgets.QComboBox(self.centralwidget)
        self.supplier_filter.setGeometry(340, 40, 200, 28)
        self.supplier_filter.addItem("Все поставщики")

        self.sort_box = QtWidgets.QComboBox(self.centralwidget)
        self.sort_box.setGeometry(560, 40, 160, 28)
        self.sort_box.addItems(["Нет сортировки", "Кол-во ↑", "Кол-во ↓"])

        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(20, 80, 960, 560)
        self.table.setColumnCount(10)
        self.table.setColumnHidden(0, True)
        self.table.setHorizontalHeaderLabels([
            "ID", "Наименование", "Категория", "Описание", "Производитель",
            "Поставщик", "Цена", "Скидка", "Кол-во", "Фото"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)

        self.btn_add = QtWidgets.QPushButton("Добавить товар", self.centralwidget)
        self.btn_add.setGeometry(20, 650, 140, 30)

        self.btn_edit = QtWidgets.QPushButton("Редактировать", self.centralwidget)
        self.btn_edit.setGeometry(170, 650, 140, 30)

        self.btn_delete = QtWidgets.QPushButton("Удалить", self.centralwidget)
        self.btn_delete.setGeometry(320, 650, 140, 30)

        # === КНОПКА "СПИСОК ЗАКАЗОВ" ===
        self.btn_orders = QtWidgets.QPushButton("Список заказов", self.centralwidget)
        self.btn_orders.setGeometry(850, 650, 130, 30)
        self.btn_orders.setVisible(False)