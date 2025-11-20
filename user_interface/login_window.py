from PyQt6 import QtWidgets, QtGui
from user_interface.products_window import ProductsWindow
from crud.users import get_user_by_login, get_all_roles

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(400, 250)
        self.setWindowIcon(QtGui.QIcon("images/Icon.png"))

        # --- Виджеты --- #
        self.label_login = QtWidgets.QLabel("Логин:", self)
        self.label_login.move(50, 50)
        self.input_login = QtWidgets.QLineEdit(self)
        self.input_login.move(150, 50)
        self.input_login.setFixedWidth(200)

        self.label_password = QtWidgets.QLabel("Пароль:", self)
        self.label_password.move(50, 100)
        self.input_password = QtWidgets.QLineEdit(self)
        self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.input_password.move(150, 100)
        self.input_password.setFixedWidth(200)

        self.button_login = QtWidgets.QPushButton("Войти", self)
        self.button_login.move(150, 150)
        self.button_login.clicked.connect(self.login)

        self.button_guest = QtWidgets.QPushButton("Войти как гость", self)
        self.button_guest.move(150, 200)
        self.button_guest.clicked.connect(self.login_as_guest)

        self.current_user = None

    def login(self):
        login_text = self.input_login.text().strip()
        password_text = self.input_password.text().strip()

        user = get_user_by_login(login_text)
        if user and user.password == password_text:
            self.current_user = user
            self.open_products_window()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def login_as_guest(self):
        self.current_user = None
        self.open_products_window()

    def open_products_window(self):
        self.products_window = ProductsWindow(user=self.current_user)
        self.products_window.show()
        self.close()
