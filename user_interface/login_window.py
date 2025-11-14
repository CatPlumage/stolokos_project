from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import pyqtSignal

from permissions import ROLE_GUEST


class LoginWindow(QWidget):
    login_success = pyqtSignal(object)  # передаём объект user

    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.setWindowTitle("Авторизация")

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.btn_login = QPushButton("Войти")
        self.btn_guest = QPushButton("Войти как гость")

        self.btn_login.clicked.connect(self.handle_login)
        self.btn_guest.clicked.connect(self.handle_guest)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Авторизация"))
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_guest)

        self.setLayout(layout)

    def handle_login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        user = self.auth_service.authenticate(login, password)
        if user:
            self.login_success.emit(user)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def handle_guest(self):
        guest_user = type("GuestUser", (), {"role": ROLE_GUEST, "name": "Гость"})()
        self.login_success.emit(guest_user)
