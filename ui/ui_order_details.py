from PyQt6 import QtWidgets, QtGui, QtCore

class Ui_OrderDetailsWindow:
    def setupUi(self, MainWindow):
        BG_DEFAULT = "#FFFFFF"
        BG_SECONDARY = "#7FFF00"
        BG_ACCENT = "#00FA9A"
        TEXT_DARK = "#000000"

        MainWindow.setWindowTitle("Детали заказа")
        MainWindow.resize(900, 600)
        MainWindow.setFixedSize(900, 600)
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
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: {BG_ACCENT};
            }}
        """)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Order info group
        self.info_group = QtWidgets.QGroupBox("Информация о заказе", self.centralwidget)
        info_layout = QtWidgets.QGridLayout(self.info_group)
        info_layout.setVerticalSpacing(5)
        info_layout.setHorizontalSpacing(10)
        
        # Create labels dictionary to store reference to value labels
        self.labels = {}
        fields = [
            ("Номер заказа:", "id"),
            ("Дата заказа:", "order_date"),
            ("Клиент:", "client"),
            ("Статус:", "status"),
            ("Пункт выдачи:", "pickup_point"),
            ("Адрес:", "address"),
            ("Код получения:", "pickup_code"),
            ("Дата доставки:", "delivery_date"),
            ("Сумма заказа:", "total_amount")
        ]
        
        for i, (label_text, field) in enumerate(fields):
            # Label
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet("font-weight: bold;")
            info_layout.addWidget(label, i, 0)
            
            # Value label
            value_label = QtWidgets.QLabel("")
            value_label.setMinimumHeight(20)
            value_label.setStyleSheet("padding: 3px; border: 1px solid #E0E0E0; border-radius: 3px;")
            self.labels[field] = value_label
            info_layout.addWidget(value_label, i, 1)
        
        self.info_group.setLayout(info_layout)
        main_layout.addWidget(self.info_group)
        
        # Products table group
        self.products_group = QtWidgets.QGroupBox("Состав заказа", self.centralwidget)
        products_layout = QtWidgets.QVBoxLayout(self.products_group)
        
        # Table
        self.products_table = QtWidgets.QTableWidget()
        self.products_table.setColumnCount(6)
        headers = ["Товар", "Артикул", "Количество", "Цена за шт.", "Скидка", "Сумма"]
        self.products_table.setHorizontalHeaderLabels(headers)
        self.products_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.products_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        
        # Column widths
        self.products_table.setColumnWidth(0, 250)  # Товар
        self.products_table.setColumnWidth(1, 100)  # Артикул
        self.products_table.setColumnWidth(2, 80)   # Количество
        self.products_table.setColumnWidth(3, 100)  # Цена
        self.products_table.setColumnWidth(4, 80)   # Скидка
        self.products_table.setColumnWidth(5, 100)  # Сумма
        
        products_layout.addWidget(self.products_table)
        
        # Total label
        self.total_label = QtWidgets.QLabel()
        self.total_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 10px;")
        self.total_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        products_layout.addWidget(self.total_label)
        
        self.products_group.setLayout(products_layout)
        main_layout.addWidget(self.products_group)
        
        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        
        # Close button
        self.btn_close = QtWidgets.QPushButton("Закрыть")
        self.btn_close.setFixedWidth(100)
        button_layout.addWidget(self.btn_close)
        
        main_layout.addLayout(button_layout)