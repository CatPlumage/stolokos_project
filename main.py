import sys
from PyQt6 import QtWidgets
from user_interface.login_window import LoginWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
