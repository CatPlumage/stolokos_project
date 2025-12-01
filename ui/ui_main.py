# ui_main.py
from PyQt6 import QtWidgets, QtGui, QtCore

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Цвета
        BG_DEFAULT = "#FFFFFF"
        BG_SECONDARY = "#7FFF00"
        BG_ACCENT = "#00FA9A"
        TEXT_DARK = "#000000"

        MainWindow.setWindowTitle("Главная — Stokolos")
        MainWindow.resize(420, 360)  # ← немного увеличили высоту окна на всякий случай
        MainWindow.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # Логотип
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(150, 20, 120, 60)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo.setPixmap(QtGui.QPixmap("images\\Icon.png").scaled(
            120, 60, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        # Приветствие
        self.label_greeting = QtWidgets.QLabel("Здравствуйте, Гость!", self.centralwidget)
        self.label_greeting.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_greeting.setGeometry(0, 90, 420, 60)  # высота 60 — для двух строк
        self.label_greeting.setWordWrap(True)
        self.label_greeting.setStyleSheet(f"""
            font-size: 14pt;
            font-weight: bold;
            color: {TEXT_DARK};
            font-family: 'Times New Roman';
        """)

        # Контейнер кнопок
        button_style = f"""
            QPushButton {{
                background-color: {BG_SECONDARY};
                color: {TEXT_DARK};
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-family: "Times New Roman";
                font-size: 10pt;
                padding: 6px;
            }}
            QPushButton:hover {{
                background-color: {BG_ACCENT};
            }}
        """

        # Позиционирование кнопок
        start_y = 160  # ← увеличенный отступ от приветствия (было 140, теперь 160)
        button_height = 36
        button_spacing = 10  # расстояние между кнопками

        self.btn_catalog = QtWidgets.QPushButton("Каталог товаров", self.centralwidget)
        self.btn_catalog.setGeometry(135, start_y, 150, button_height)
        self.btn_catalog.setStyleSheet(button_style)

        self.btn_orders = QtWidgets.QPushButton("Список заказов", self.centralwidget)
        self.btn_orders.setGeometry(135, start_y + button_height + button_spacing, 150, button_height)
        self.btn_orders.setStyleSheet(button_style)
        self.btn_orders.setVisible(False)

        self.btn_logout = QtWidgets.QPushButton("Выход", self.centralwidget)
        self.btn_logout.setGeometry(135, start_y + 2 * (button_height + button_spacing), 150, button_height)
        self.btn_logout.setStyleSheet(button_style)