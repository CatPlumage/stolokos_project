from PyQt6 import QtWidgets, QtGui, QtCore

class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        # Цвета
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
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # Логотип
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(150, 10, 120, 60)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo.setPixmap(QtGui.QPixmap("images\\Icon.png").scaled(
            120, 60, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        # Контейнер формы
        self.form_frame = QtWidgets.QFrame(self.centralwidget)
        self.form_frame.setGeometry(40, 80, 340, 110)
        self.form_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_SECONDARY};
                border-radius: 10px;
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
        """)

        # Заголовок
        self.label_title = QtWidgets.QLabel("Авторизация", self.form_frame)
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_title.setGeometry(0, 10, 340, 24)
        self.label_title.setStyleSheet(f"font-weight: bold; font-size: 14pt; color: {TEXT_DARK}; font-family: 'Times New Roman';")

        # Поля ввода и метки
        self.label_login = QtWidgets.QLabel("Логин:", self.form_frame)
        self.label_login.setGeometry(20, 45, 60, 20)
        self.label_login.setStyleSheet(f"color: {TEXT_DARK}; font-family: 'Times New Roman';")

        self.input_login = QtWidgets.QLineEdit(self.form_frame)
        self.input_login.setGeometry(90, 45, 230, 20)
        self.input_login.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 2px 4px;
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
        """)

        self.label_password = QtWidgets.QLabel("Пароль:", self.form_frame)
        self.label_password.setGeometry(20, 75, 60, 20)
        self.label_password.setStyleSheet(f"color: {TEXT_DARK}; font-family: 'Times New Roman';")

        self.input_password = QtWidgets.QLineEdit(self.form_frame)
        self.input_password.setGeometry(90, 75, 230, 20)
        self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.input_password.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_DEFAULT};
                color: {TEXT_DARK};
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 2px 4px;
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
        """)

        # Стиль кнопок
        button_style = f"""
            QPushButton {{
                background-color: {BG_SECONDARY};
                color: {TEXT_DARK};
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-family: "Times New Roman";
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {BG_ACCENT};
            }}
        """

        self.btn_login = QtWidgets.QPushButton("Войти", self.centralwidget)
        self.btn_login.setGeometry(120, 200, 110, 32)
        self.btn_login.setStyleSheet(button_style)

        self.btn_guest = QtWidgets.QPushButton("Войти как гость", self.centralwidget)
        self.btn_guest.setGeometry(260, 200, 110, 32)
        self.btn_guest.setStyleSheet(button_style)