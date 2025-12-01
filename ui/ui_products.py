from PyQt6 import QtWidgets, QtGui, QtCore

class Ui_ProductsWindow(object):
    def setupUi(self, MainWindow):
        # Цвета
        BG_DEFAULT = "#FFFFFF"     # белый фон
        BG_SECONDARY = "#7FFF00"   # chartreuse — для кнопок
        BG_ACCENT = "#00FA9A"      # spring green — hover и выделение
        TEXT_DARK = "#000000"      # чёрный текст — ВСЕГДА

        MainWindow.setWindowTitle("Каталог товаров — Stokolos")
        MainWindow.resize(1000, 700)

        # Глобальный стиль: принудительно белый фон + чёрный текст для всего окна
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
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        # === Метка пользователя ===
        self.label_user = QtWidgets.QLabel("Гость", self.centralwidget)
        self.label_user.setGeometry(650, 10, 400, 25)
        # Явно задаём стиль, чтобы избежать наследования системного цвета
        self.label_user.setStyleSheet(f"color: {TEXT_DARK}; font-family: 'Times New Roman'; font-size: 9pt;")

        self.btn_back = QtWidgets.QPushButton("Назад", self.centralwidget)
        self.btn_back.setGeometry(10, 10, 70, 25)
        self.btn_back.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_SECONDARY};
                color: {TEXT_DARK};
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-family: "Times New Roman";
                font-size: 8pt;
            }}
            QPushButton:hover {{
                background-color: {BG_ACCENT};
            }}
        """)

        # === Поле поиска ===
        self.search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_input.setGeometry(20, 40, 300, 28)
        self.search_input.setPlaceholderText("Поиск... (название, описание, производитель...)")
        self.search_input.setStyleSheet(f"""
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
        """)

        # === Выпадающие списки ===
        combo_style = f"""
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
        """

        self.supplier_filter = QtWidgets.QComboBox(self.centralwidget)
        self.supplier_filter.setGeometry(340, 40, 200, 28)
        self.supplier_filter.addItem("Все поставщики")
        self.supplier_filter.setStyleSheet(combo_style)

        self.sort_box = QtWidgets.QComboBox(self.centralwidget)
        self.sort_box.setGeometry(560, 40, 160, 28)
        self.sort_box.addItems(["Нет сортировки", "Кол-во ↑", "Кол-во ↓"])
        self.sort_box.setStyleSheet(combo_style)

        # === Таблица ===
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

        self.table.setStyleSheet(f"""
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
        """)

        # === Кнопки администратора ===
        button_style = f"""
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
        """

        self.btn_add = QtWidgets.QPushButton("Добавить товар", self.centralwidget)
        self.btn_add.setGeometry(20, 650, 140, 30)
        self.btn_add.setStyleSheet(button_style)

        self.btn_edit = QtWidgets.QPushButton("Редактировать", self.centralwidget)
        self.btn_edit.setGeometry(170, 650, 140, 30)
        self.btn_edit.setStyleSheet(button_style)

        self.btn_delete = QtWidgets.QPushButton("Удалить", self.centralwidget)
        self.btn_delete.setGeometry(320, 650, 140, 30)
        self.btn_delete.setStyleSheet(button_style)

        MainWindow.setCentralWidget(self.centralwidget)