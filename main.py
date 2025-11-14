import sys
from PyQt6.QtWidgets import QApplication
from login_window import AuthWindow
from search_window import SearchWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.auth_window = AuthWindow()
        self.search_window = None
        
        # Подключаем сигнал
        self.auth_window.login_success.connect(self.show_search_window)
        
    def show_search_window(self, username):
        # Скрываем окно авторизации
        self.auth_window.hide()
        
        # Создаем и показываем окно поиска
        self.search_window = SearchWindow(username)
        self.search_window.show()
        
    def run(self):
        self.auth_window.show()
        return self.app.exec()

if __name__ == "__main__":
    controller = AppController()
    sys.exit(controller.run())