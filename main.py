import sys
from PyQt6 import QtWidgets
from user_interface.login_window import LoginWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
