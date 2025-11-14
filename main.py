from PyQt6.QtWidgets import QApplication
from user_interface.login_window import LoginWindow
from user_interface.products_window import ProductsWindow
import sys

class FakeAuthService:
    """Примерная логика авторизации"""
    def authenticate(self, login, password):
        roles = {
            "user": "user",
            "manager": "manager",
            "admin": "admin",
        }

        role = roles.get(login)
        if role and password == "123":
            return type("User", (), {"role": role, "name": login})()

        return None


def main():
    app = QApplication(sys.argv)

    auth = FakeAuthService()
    login = LoginWindow(auth)

    def on_login(user):
        products = ProductsWindow(user)
        products.show()
        login.close()

    login.login_success.connect(on_login)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
