# ui_orders.py
from PyQt6 import QtWidgets, QtGui, QtCore

class Ui_OrdersWindow:
    def setupUi(self, MainWindow):
        BG_DEFAULT = "#FFFFFF"
        BG_SECONDARY = "#7FFF00"
        BG_ACCENT = "#00FA9A"
        BG_SELECTED = BG_ACCENT  # Цвет выделения
        BG_SCROLL_AREA = "#F0F0F0"  # Светло-серый фон для области прокрутки
        TEXT_DARK = "#000000"

        MainWindow.setWindowTitle("Управление заказами — Stokolos")
        MainWindow.resize(1400, 700)
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
            QGroupBox {{
                font-weight: bold;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                margin-top: 10px;
                font-family: "Times New Roman";
                font-size: 9pt;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
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
            QDateEdit {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 2px 6px;
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
            QScrollArea QWidget {{  /* Widget внутри ScrollArea */
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
            /* Стиль для статусбара */
            QStatusBar {{
                background-color: #F0F0F0;
                color: {TEXT_DARK};
                font-family: "Times New Roman";
                font-size: 8pt;
            }}
        """)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        # User info label
        self.label_user = QtWidgets.QLabel("Гость", self.centralwidget)
        self.label_user.setGeometry(1100, 10, 300, 25)
        self.label_user.setStyleSheet("font-weight: bold;")
        
        # Back button
        self.btn_back = QtWidgets.QPushButton("Назад", self.centralwidget)
        self.btn_back.setGeometry(10, 10, 70, 25)
        
        # Filter group
        self.filter_group = QtWidgets.QGroupBox("Фильтры", self.centralwidget)
        self.filter_group.setGeometry(10, 40, 1380, 100)
        
        # Client search
        self.label_client = QtWidgets.QLabel("Клиент:", self.filter_group)
        self.label_client.setGeometry(10, 40, 50, 25)
        
        self.client_search = QtWidgets.QLineEdit(self.filter_group)
        self.client_search.setGeometry(70, 40, 300, 25)
        self.client_search.setPlaceholderText("Поиск по имени клиента...")
        
        # Apply/Reset buttons
        self.btn_apply = QtWidgets.QPushButton("Применить фильтры", self.filter_group)
        self.btn_apply.setGeometry(400, 40, 140, 25)
        
        self.btn_reset = QtWidgets.QPushButton("Сбросить", self.filter_group)
        self.btn_reset.setGeometry(550, 40, 100, 25)
        
        # Button panel
        self.btn_refresh = QtWidgets.QPushButton("Обновить", self.centralwidget)
        self.btn_refresh.setGeometry(10, 150, 100, 30)
        
        # Кнопки действий с заказами
        self.btn_add = QtWidgets.QPushButton("Добавить заказ", self.centralwidget)
        self.btn_add.setGeometry(120, 150, 140, 30)
        
        self.btn_delete = QtWidgets.QPushButton("Удалить заказ", self.centralwidget)
        self.btn_delete.setGeometry(270, 150, 140, 30)  # Сдвинуто на место редактирования
        self.btn_delete.setEnabled(False)
        
        # Кнопка просмотра деталей
        self.btn_view_details = QtWidgets.QPushButton("Просмотреть детали", self.centralwidget)
        self.btn_view_details.setGeometry(420, 150, 140, 30)  # Сдвинуто на место удаления
        self.btn_view_details.setEnabled(False)
        
        # Заменяем таблицу на ScrollArea для карточек
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setGeometry(10, 190, 1380, 450)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        
        # Вертикальный layout для карточек
        self.cards_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.cards_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.cards_layout.setSpacing(10)
        self.cards_layout.setContentsMargins(5, 5, 5, 5)
        
        # Status bar
        MainWindow.setStatusBar(QtWidgets.QStatusBar(MainWindow))