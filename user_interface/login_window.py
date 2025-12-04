import os
from PyQt6 import QtWidgets
from ui.ui_login import Ui_LoginWindow
from crud.users import get_user_by_login

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.btn_login.clicked.connect(self.handle_login)
        self.ui.btn_guest.clicked.connect(self.handle_guest)

    def handle_login(self):
        login = self.ui.input_login.text().strip()
        password = self.ui.input_password.text().strip()
        if not login or not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        user = get_user_by_login(login)
        if user is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return
        if user.password != password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный пароль")
            return
        self.open_products_window(user)

    def handle_guest(self):
        self.open_products_window(None)

    def open_products_window(self, user):
        from user_interface.products_window import ProductsWindow
        self.products_window = ProductsWindow(user=user)
        self.products_window.show()
        self.close()