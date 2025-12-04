# ui_product_edit.py (обновлённый)
from PyQt6 import QtWidgets, QtCore

class Ui_ProductEditWindow:
    def setupUi(self, Dialog):
        BG_DEFAULT = "#FFFFFF"
        BG_SECONDARY = "#7FFF00"
        BG_ACCENT = "#00FA9A"
        TEXT_DARK = "#000000"

        Dialog.setWindowTitle("Добавить / Редактировать товар")
        Dialog.resize(600, 480)
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
            QLineEdit, QComboBox, QTextEdit, QSpinBox, QDoubleSpinBox {{
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
        self.formLayout = QtWidgets.QFormLayout()

        self.input_name = QtWidgets.QLineEdit()
        self.cmb_category = QtWidgets.QComboBox()
        self.cmb_manufacturer = QtWidgets.QComboBox()
        self.cmb_supplier = QtWidgets.QComboBox()
        self.input_price = QtWidgets.QDoubleSpinBox()
        self.input_price.setMaximum(1e9)
        self.input_price.setDecimals(2)
        self.input_quantity = QtWidgets.QSpinBox()
        self.input_quantity.setMaximum(10**6)
        self.input_discount = QtWidgets.QDoubleSpinBox()
        self.input_discount.setRange(0, 100)
        self.input_discount.setDecimals(2)
        self.input_description = QtWidgets.QTextEdit()
        self.input_description.setMaximumHeight(80)

        self.lbl_image = QtWidgets.QLabel()
        self.lbl_image.setFixedSize(300, 200)
        self.lbl_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.btn_choose_image = QtWidgets.QPushButton("Выбрать изображение")
        self.btn_remove_image = QtWidgets.QPushButton("Удалить изображение")

        self.formLayout.addRow("Наименование:", self.input_name)
        self.formLayout.addRow("Категория:", self.cmb_category)
        self.formLayout.addRow("Производитель:", self.cmb_manufacturer)
        self.formLayout.addRow("Поставщик:", self.cmb_supplier)
        self.formLayout.addRow("Цена:", self.input_price)
        self.formLayout.addRow("Количество:", self.input_quantity)
        self.formLayout.addRow("Скидка %:", self.input_discount)
        self.formLayout.addRow("Описание:", self.input_description)
        self.formLayout.addRow("Фото (макс 300x200):", self.lbl_image)
        self.formLayout.addRow("", self.btn_choose_image)
        self.formLayout.addRow("", self.btn_remove_image)

        self.verticalLayout.addLayout(self.formLayout)

        self.btns_layout = QtWidgets.QHBoxLayout()
        self.btn_save = QtWidgets.QPushButton("Сохранить")
        self.btn_cancel = QtWidgets.QPushButton("Отмена")
        self.btns_layout.addWidget(self.btn_save)
        self.btns_layout.addWidget(self.btn_cancel)

        self.verticalLayout.addLayout(self.btns_layout)