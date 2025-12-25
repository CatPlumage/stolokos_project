# ui_products.py
from PyQt6 import QtWidgets, QtGui, QtCore

class Ui_ProductsWindow:
    def setupUi(self, MainWindow):
        BG_DEFAULT = "#FFFFFF"
        BG_SECONDARY = "#7FFF00"
        BG_ACCENT = "#00FA9A"
        BG_SELECTED = BG_ACCENT
        BG_SCROLL_AREA = "#F0F0F0"  # Светло-серый фон для области прокрутки
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
            QPushButton:disabled {{
                background-color: #CCCCCC;
                color: #666666;
            }}
            QScrollArea {{
                border: none;
                background-color: {BG_SCROLL_AREA};
            }}
            QScrollArea QWidget {{
                background-color: {BG_SCROLL_AREA};
            }}
            QWidget#card_widget {{
                background-color: {BG_DEFAULT};
                border: 1px solid #DDDDDD;
                border-radius: 8px;
                margin: 5px;
            }}
            QWidget#card_widget:hover {{
                border-color: #AAAAAA;
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

        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setGeometry(20, 80, 960, 560)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        
        self.cards_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.cards_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.cards_layout.setSpacing(10)
        self.cards_layout.setContentsMargins(5, 5, 5, 5)

        self.btn_add = QtWidgets.QPushButton("Добавить товар", self.centralwidget)
        self.btn_add.setGeometry(20, 650, 140, 30)

        self.btn_delete = QtWidgets.QPushButton("Удалить", self.centralwidget)
        self.btn_delete.setGeometry(170, 650, 140, 30)  # Сдвинуто влево
        self.btn_delete.setEnabled(False)

        # === КНОПКА "СПИСОК ЗАКАЗОВ" ===
        self.btn_orders = QtWidgets.QPushButton("Список заказов", self.centralwidget)
        self.btn_orders.setGeometry(850, 650, 130, 30)
        self.btn_orders.setVisible(False)