import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QListWidget
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from crud.authorization import get_user_by_login

class BaseWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(700, 520)
        self.setStyleSheet("""
            background-color: #FFFFFF;
            color: #000000;
            font-family: 'Times New Roman';
        """)
 
    def add_back_button(self, parent_window):
        btn = QPushButton("⬅ Назад")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                padding: 8px;
                font-size: 14px;
                border-radius: 6px;
                color: black;
                max-width: 140px;
            }
            QPushButton:hover { background-color: #00FA9A; }
        """)
        btn.clicked.connect(lambda: (self.close(), parent_window.show()))
        return btn
 
class ProductView(BaseWindow):
    def __init__(self, role, parent):
        super().__init__("Каталог товаров")
        self.role = role
        self.parent = parent
 
        layout = QVBoxLayout()
        title = QLabel(f"Каталог товаров — роль: {role}")
        title.setFont(QFont("Times New Roman", 20))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
 
        self.list = QListWidget()
        demo_products = [
            "Кроссовки Nike Air",
            "Туфли на каблуке PinkHeels",
            "Ботинки зимние Nord",
            "Сандалии летние Breeze",
        ]
        self.list.addItems(demo_products)
        layout.addWidget(self.list)
 
        layout.addWidget(self.add_back_button(self.parent))
        self.setLayout(layout)
 
class OrderView(BaseWindow):
    def __init__(self, parent):
        super().__init__("Список заказов")
        self.parent = parent
        layout = QVBoxLayout()
        title = QLabel("Заказы")
        title.setFont(QFont("Times New Roman", 20))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
 
        demo_orders = ["#1001 — Nike Air", "#1002 — PinkHeels"]
        listw = QListWidget()
        listw.addItems(demo_orders)
        layout.addWidget(listw)
 
        layout.addWidget(self.add_back_button(self.parent))
        self.setLayout(layout)
 
class RoleMenu(BaseWindow):
    def __init__(self, role, fullname, parent):
        super().__init__("Меню навигации")
        self.role = role
        self.fullname = fullname
        self.parent = parent
 
        layout = QVBoxLayout()
        header = QLabel(f"Добро пожаловать, {fullname}!\nРоль: {role}")
        header.setFont(QFont("Times New Roman", 18))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
 
        if role in ("Авторизированный клиент", "Клиент"):
            btn = QPushButton("Просмотр товаров")
            btn.clicked.connect(self.open_products_simple)
            layout.addWidget(btn)
 
        if role == "Менеджер":
            b1 = QPushButton("Просмотр товаров (расширенный)")
            b1.clicked.connect(self.open_products_advanced)
            layout.addWidget(b1)
            b2 = QPushButton("Просмотр заказов")
            b2.clicked.connect(self.open_orders)
            layout.addWidget(b2)
 
        if role == "Администратор":
            b1 = QPushButton("Управление товарами (CRUD)")
            b1.clicked.connect(self.open_products_advanced)
            layout.addWidget(b1)
            b2 = QPushButton("Управление заказами (CRUD)")
            b2.clicked.connect(self.open_orders)
            layout.addWidget(b2)
 
        for w in layout.children():
            pass
 
        for child in self.findChildren(QPushButton):
            child.setStyleSheet("""
                QPushButton {
                    background-color: #00FA9A;
                    padding: 12px;
                    font-size: 16px;
                    border-radius: 6px;
                    color: #000000;
                }
                QPushButton:hover { background-color: #7FFF00; }
            """)
 
        layout.addWidget(self.add_back_button(self.parent))
        self.setLayout(layout)
 
    def open_products_simple(self):
        self.hide()
        self.child = ProductView("Клиент", self)
        self.child.show()
 
    def open_products_advanced(self):
        self.hide()
        self.child = ProductView("Расширенный доступ (менеджер/админ)", self)
        self.child.show()
 
    def open_orders(self):
        self.hide()
        self.child = OrderView(self)
        self.child.show()
 
class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__("Вход в систему")
 
        main = QVBoxLayout()
 
        image_label = QLabel()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        png_path = os.path.join(current_dir, "welcome.png")
        pix = QPixmap(png_path)
        if not pix.isNull():
            pix = pix.scaled(420, 280, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pix)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(image_label)
 
        title = QLabel("Пожалуйста, авторизуйтесь")
        title.setFont(QFont("Times New Roman", 22))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(title)
 
        # Поля логина/пароля
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин (email)")
        self.login_input.setStyleSheet("padding: 8px; font-size: 16px;")
        main.addWidget(self.login_input)
 
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setStyleSheet("padding: 8px; font-size: 16px;")
        main.addWidget(self.pass_input)
 
        btn_row = QHBoxLayout()
        btn_login = QPushButton("Войти")
        btn_guest = QPushButton("Войти как гость")
 
        for btn in (btn_login, btn_guest):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #00FA9A;
                    padding: 10px;
                    font-size: 15px;
                    border-radius: 6px;
                }
                QPushButton:hover { background-color: #7FFF00; }
            """)
 
        btn_row.addWidget(btn_login)
        btn_row.addWidget(btn_guest)
        main.addLayout(btn_row)
 
        self.setLayout(main)
 
        # Сигналы
        btn_login.clicked.connect(self.handle_login)
        btn_guest.clicked.connect(self.handle_guest)
 
    def handle_login(self):
        login = self.login_input.text().strip()
        password = self.pass_input.text().strip()
 
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
 
        user = get_user_by_login(login)
        if user is None:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return
 
        role = user.role.name if user.role else None
        fullname = user.full_name
        real_password = user.password

        if password != real_password:
            QMessageBox.warning(self, "Ошибка", "Неверный пароль")
            return
 
        # Успешный вход
        self.hide()
        self.child = RoleMenu(role, fullname, self)
        self.child.show()
 
    def handle_guest(self):
        self.hide()
        self.child = ProductView("Гость", self)
        self.child.show()
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())