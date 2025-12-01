# main_window.py
from PyQt6 import QtWidgets
from ui.ui_main import Ui_MainWindow
from user_interface.products_window import ProductsWindow

from user_interface.login_window import LoginWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user = user

        # Установка приветствия
        if user:
            self.ui.label_greeting.setText(f"Здравствуйте, {user.full_name}!")
            role = user.role.name if user.role else "guest"
            if role in ("Администратор", "Менеджер"):
                self.ui.btn_orders.setVisible(True)
        else:
            self.ui.label_greeting.setText("Здравствуйте, Гость!")

        # Подключение кнопок
        self.ui.btn_catalog.clicked.connect(self.open_products)
        self.ui.btn_logout.clicked.connect(self.logout)

        self.products_window = None
        self.orders_window = None

    def open_products(self):
        self.products_window = ProductsWindow(user=self.user, parent_main=self)
        self.products_window.show()
        self.close()


    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()