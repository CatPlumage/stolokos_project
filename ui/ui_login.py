# ui_login.py
from PyQt6 import QtWidgets, QtGui, QtCore

class Ui_LoginWindow:
    def setupUi(self, MainWindow):
        BG_DEFAULT = "#FFFFFF"
        BG_SECONDARY = "#7FFF00"
        BG_ACCENT = "#00FA9A"
        TEXT_DARK = "#000000"

        MainWindow.setWindowTitle("Авторизация — Stokolos")
        MainWindow.resize(420, 260)
        MainWindow.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
            QLabel {{
                color: {TEXT_DARK};
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
            QLineEdit {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 2px 4px;
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
            QLineEdit:focus {{
                border: 1px solid #000000;
            }}
            QFrame {{
                background-color: {BG_SECONDARY};
                border-radius: 10px;
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
            QPushButton {{
                background-color: {BG_SECONDARY};
                color: {TEXT_DARK};
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-family: "Times New Roman";
                font-size: 10pt;
                padding: 6px;
            }}
            QPushButton:hover {{
                background-color: {BG_ACCENT};
            }}
            /* Стиль для всех QMessageBox */
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

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(150, 10, 120, 60)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo.setPixmap(QtGui.QPixmap("images\\Icon.png").scaled(
            120, 60, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.logo.setStyleSheet(f"background-color: {BG_DEFAULT}; border: none;")

        self.form_frame = QtWidgets.QFrame(self.centralwidget)
        self.form_frame.setGeometry(40, 80, 340, 110)

        self.label_title = QtWidgets.QLabel("Авторизация", self.form_frame)
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_title.setGeometry(0, 10, 340, 24)
        self.label_title.setStyleSheet("font-weight: bold; font-size: 14pt;")

        self.label_login = QtWidgets.QLabel("Логин:", self.form_frame)
        self.label_login.setGeometry(20, 45, 60, 20)

        self.input_login = QtWidgets.QLineEdit(self.form_frame)
        self.input_login.setGeometry(90, 45, 230, 20)

        self.label_password = QtWidgets.QLabel("Пароль:", self.form_frame)
        self.label_password.setGeometry(20, 75, 60, 20)

        self.input_password = QtWidgets.QLineEdit(self.form_frame)
        self.input_password.setGeometry(90, 75, 230, 20)
        self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.btn_login = QtWidgets.QPushButton("Войти", self.centralwidget)
        self.btn_login.setGeometry(120, 200, 110, 32)

        self.btn_guest = QtWidgets.QPushButton("Войти как гость", self.centralwidget)
        self.btn_guest.setGeometry(260, 200, 110, 32)