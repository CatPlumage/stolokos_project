# ui_orders.py
from PyQt6 import QtWidgets, QtGui, QtCore

class Ui_OrdersWindow:
    def setupUi(self, MainWindow):
        BG_DEFAULT = "#FFFFFF"
        BG_SECONDARY = "#7FFF00"
        BG_ACCENT = "#00FA9A"
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
            /* Стиль для выделенной строки */
            QTableWidget::item:selected {{
                background-color: {BG_ACCENT};
                color: {TEXT_DARK};
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
        
        # Status filter
        self.label_status = QtWidgets.QLabel("Статус:", self.filter_group)
        self.label_status.setGeometry(10, 25, 50, 25)
        
        self.status_combo = QtWidgets.QComboBox(self.filter_group)
        self.status_combo.setGeometry(70, 25, 150, 25)
        self.status_combo.addItem("Все статусы")
        
        # Date from
        self.label_date_from = QtWidgets.QLabel("С:", self.filter_group)
        self.label_date_from.setGeometry(240, 25, 20, 25)
        
        self.date_from = QtWidgets.QDateEdit(self.filter_group)
        self.date_from.setGeometry(260, 25, 120, 25)
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QtCore.QDate.currentDate().addMonths(-1))
        
        # Date to
        self.label_date_to = QtWidgets.QLabel("По:", self.filter_group)
        self.label_date_to.setGeometry(400, 25, 30, 25)
        
        self.date_to = QtWidgets.QDateEdit(self.filter_group)
        self.date_to.setGeometry(430, 25, 120, 25)
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QtCore.QDate.currentDate())
        
        # Client search
        self.label_client = QtWidgets.QLabel("Клиент:", self.filter_group)
        self.label_client.setGeometry(10, 60, 50, 25)
        
        self.client_search = QtWidgets.QLineEdit(self.filter_group)
        self.client_search.setGeometry(70, 60, 300, 25)
        self.client_search.setPlaceholderText("Поиск по имени клиента...")
        
        # Apply/Reset buttons
        self.btn_apply = QtWidgets.QPushButton("Применить фильтры", self.filter_group)
        self.btn_apply.setGeometry(400, 60, 140, 25)
        
        self.btn_reset = QtWidgets.QPushButton("Сбросить", self.filter_group)
        self.btn_reset.setGeometry(550, 60, 100, 25)
        
        # Button panel - УПОРЯДОЧИМ КНОПКИ
        self.btn_refresh = QtWidgets.QPushButton("Обновить", self.centralwidget)
        self.btn_refresh.setGeometry(10, 150, 100, 30)
        
        # Новые кнопки: Добавить, Редактировать, Удалить - в одном ряду
        self.btn_add = QtWidgets.QPushButton("Добавить заказ", self.centralwidget)
        self.btn_add.setGeometry(120, 150, 140, 30)
        
        self.btn_edit = QtWidgets.QPushButton("Редактировать заказ", self.centralwidget)
        self.btn_edit.setGeometry(270, 150, 140, 30)
        
        self.btn_delete = QtWidgets.QPushButton("Удалить заказ", self.centralwidget)
        self.btn_delete.setGeometry(420, 150, 140, 30)
        
        # Кнопка просмотра деталей
        self.btn_view_details = QtWidgets.QPushButton("Просмотреть детали", self.centralwidget)
        self.btn_view_details.setGeometry(570, 150, 140, 30)
        
        # Table
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(10, 190, 1380, 450)
        self.table.setColumnCount(8)
        headers = [
            "ID", "Дата заказа", "Клиент",
            "Сумма заказа", "Статус", "Пункт выдачи", 
            "Код получения", "Товаров"
        ]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Column widths
        self.table.setColumnWidth(0, 50)   # ID
        self.table.setColumnWidth(1, 100)  # Дата
        self.table.setColumnWidth(2, 200)  # Клиент
        self.table.setColumnWidth(3, 120)  # Сумма
        self.table.setColumnWidth(4, 120)  # Статус
        self.table.setColumnWidth(5, 250)  # Пункт выдачи
        self.table.setColumnWidth(6, 100)  # Код
        self.table.setColumnWidth(7, 80)   # Товаров
        
        # Status bar
        MainWindow.setStatusBar(QtWidgets.QStatusBar(MainWindow))