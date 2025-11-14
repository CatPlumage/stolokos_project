# products_window.py
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.ui_products import ProductsWindow  # твой класс из ui_products.py

class ProductsWindowUI(QMainWindow):
    def __init__(self, role: str, parent=None):
        super().__init__(parent)
        self.role = role
        self.ui = ProductsWindow()
        self.ui.setupUi(self)

        # Настраиваем функционал в зависимости от роли
        self.configure_role_permissions()

        # Подключаем кнопку "Назад"
        self.ui.pushButton.clicked.connect(self.go_back)

    def configure_role_permissions(self):
        """
        Настройка видимости и функционала кнопок в зависимости от роли.
        """
        if self.role in ("Неавторизованный", "Гость"):
            # Только просмотр товаров
            self.disable_advanced_features()
        elif self.role == "Авторизированный клиент":
            self.disable_advanced_features()
            # Можно оставить кнопки для просмотра, если нужно
        elif self.role == "Менеджер":
            # Доступ к фильтрам, сортировке, поиску
            self.enable_filters_sort_search()
            self.disable_admin_crud()
        elif self.role == "Администратор":
            # Полный доступ
            self.enable_filters_sort_search()
            self.enable_admin_crud()
        else:
            QMessageBox.warning(self, "Ошибка", f"Неизвестная роль: {self.role}")

    def disable_advanced_features(self):
        """
        Скрываем/отключаем все кнопки CRUD, фильтры, сортировку, поиск.
        """
        self.ui.pushButton_5.setEnabled(False)  # Удалить
        self.ui.pushButton_6.setEnabled(False)  # Сохранить
        self.ui.pushButton_7.setEnabled(False)  # Удалить (2-й товар)
        self.ui.pushButton_8.setEnabled(False)  # Сохранить (2-й товар)
        self.ui.pushButton_9.setEnabled(False)  # Удалить (3-й товар)
        self.ui.pushButton_10.setEnabled(False) # Сохранить (3-й товар)
        self.ui.pushButton_11.setEnabled(False) # Добавить
        self.ui.pushButton_12.setEnabled(False) # Фильтры
        self.ui.pushButton_13.setEnabled(False) # Сортировка
        self.ui.keySequenceEdit.setEnabled(False) # Поиск

    def enable_filters_sort_search(self):
        self.ui.pushButton_12.setEnabled(True)  # Фильтры
        self.ui.pushButton_13.setEnabled(True)  # Сортировка
        self.ui.keySequenceEdit.setEnabled(True) # Поиск

    def enable_admin_crud(self):
        self.ui.pushButton_5.setEnabled(True)  # Удалить
        self.ui.pushButton_6.setEnabled(True)  # Сохранить
        self.ui.pushButton_7.setEnabled(True)
        self.ui.pushButton_8.setEnabled(True)
        self.ui.pushButton_9.setEnabled(True)
        self.ui.pushButton_10.setEnabled(True)
        self.ui.pushButton_11.setEnabled(True)  # Добавить

    def disable_admin_crud(self):
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_10.setEnabled(False)
        self.ui.pushButton_11.setEnabled(False)

    def go_back(self):
        """
        Возврат к родительскому окну (например, LoginWindow)
        """
        self.close()
        if self.parent():
            self.parent().show()
