# user_interface/orders_window.py
import os
from datetime import datetime
from PyQt6 import QtWidgets, QtGui, QtCore
from ui.ui_orders import Ui_OrdersWindow

from crud.orders import get_all_orders, update_order, delete_order
from crud.references import get_all_order_statuses, get_all_pickup_points
from user_interface.order_details_window import OrderDetailsWindow
from user_interface.order_edit_window import OrderEditWindow

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class OrdersWindow(QtWidgets.QMainWindow):
    def __init__(self, user=None, parent_main=None):
        super().__init__()
        self.ui = Ui_OrdersWindow()
        self.ui.setupUi(self)
        
        self.user = user
        self.parent_main = parent_main
        self._orders_cache = []
        self._details_window = None
        self._edit_window = None
        
        # Настройка прав доступа
        self.setup_role_permissions()
        
        # Загрузка фильтров
        self.load_filters()
        
        # Загрузка заказов
        self.load_orders()
        
        # Подключение сигналов
        self.setup_connections()
        
    def setup_connections(self):
        """Подключение всех сигналов"""
        self.ui.btn_back.clicked.connect(self.go_back)
        self.ui.btn_apply.clicked.connect(self.apply_filters)
        self.ui.btn_reset.clicked.connect(self.reset_filters)
        self.ui.btn_refresh.clicked.connect(self.refresh_orders)
        self.ui.btn_add.clicked.connect(self.add_order)
        self.ui.btn_edit.clicked.connect(self.edit_order)
        self.ui.btn_view_details.clicked.connect(self.view_order_details)
        self.ui.btn_delete.clicked.connect(self.delete_selected_order)
        self.ui.table.cellDoubleClicked.connect(self.on_table_double_click)
        self.ui.client_search.textChanged.connect(self.apply_filters)
        
    def setup_role_permissions(self):
        """Настройка прав доступа в зависимости от роли"""
        role_name = self.user.role.name if self.user and self.user.role else "guest"
        self.role_name = role_name
        
        # Показываем пользователя
        if self.user:
            self.ui.label_user.setText(f"{self.user.full_name} ({role_name})")
        else:
            self.ui.label_user.setText("Гость")
        
        # Настройка видимости элементов по ролям
        is_admin = role_name == "Администратор"
        is_manager = role_name == "Менеджер"
        is_client = role_name == "Авторизированный клиент"
        
        # Фильтры видны менеджерам и админам
        self.ui.status_combo.setVisible(is_manager or is_admin)
        self.ui.date_from.setVisible(is_manager or is_admin)
        self.ui.date_to.setVisible(is_manager or is_admin)
        self.ui.client_search.setVisible(is_manager or is_admin)
        self.ui.btn_apply.setVisible(is_manager or is_admin)
        self.ui.btn_reset.setVisible(is_manager or is_admin)
        self.ui.label_status.setVisible(is_manager or is_admin)
        self.ui.label_date_from.setVisible(is_manager or is_admin)
        self.ui.label_date_to.setVisible(is_manager or is_admin)
        self.ui.label_client.setVisible(is_manager or is_admin)
        
        # Кнопки действий
        self.ui.btn_add.setVisible(is_admin)
        self.ui.btn_edit.setVisible(is_admin)
        self.ui.btn_delete.setVisible(is_admin)
        
        # Если клиент, показываем только его заказы
        self.show_only_user_orders = is_client
        
    def load_filters(self):
        """Загрузка данных для фильтров"""
        try:
            # Очищаем комбобокс перед загрузкой (чтобы избежать дублирования)
            self.ui.status_combo.clear()
            self.ui.status_combo.addItem("Все статусы")
            
            # Загружаем статусы
            statuses = get_all_order_statuses()
            for status in statuses:
                self.ui.status_combo.addItem(status.name)
            
            # Загружаем пункты выдачи
            self.pickup_points = get_all_pickup_points()
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить фильтры: {e}")
    
    def load_orders(self):
        """Загрузка всех заказов из базы"""
        try:
            # Получаем все заказы с связанными данными
            self._orders_cache = get_all_orders()
            
            # Если клиент, показываем только его заказы
            if self.show_only_user_orders and self.user:
                self._orders_cache = [order for order in self._orders_cache 
                                    if order.user_id == self.user.id]
            
            # Применяем текущие фильтры
            self.apply_filters()
            
            # Показываем сообщение об успешной загрузке
            self.statusBar().showMessage(f"Загружено {len(self._orders_cache)} заказов")
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить заказы: {e}")
            self.statusBar().showMessage("Ошибка загрузки заказов")
    
    def refresh_orders(self):
        """Обновление списка заказов (вызывается по кнопке Обновить)"""
        try:
            
            # Очищаем кэш перед загрузкой
            self._orders_cache = []
            
            # Загружаем заказы заново
            self._orders_cache = get_all_orders()

            # Если клиент, показываем только его заказы
            if self.show_only_user_orders and self.user:
                self._orders_cache = [order for order in self._orders_cache 
                                    if order.user_id == self.user.id]
            
            # Применяем текущие фильтры
            self.apply_filters()
            
            # Показываем сообщение об успешном обновлении
            self.statusBar().showMessage(f"Данные обновлены. Загружено {len(self._orders_cache)} заказов", 3000)
            
        except Exception as e:
            error_msg = f"Не удалось обновить заказы: {str(e)}"
            QtWidgets.QMessageBox.critical(self, "Ошибка", error_msg)
            self.statusBar().showMessage("Ошибка обновления")
    
    def apply_filters(self):
        """Применение фильтров к загруженным заказам"""
        if not self._orders_cache:
            self.ui.table.setRowCount(0)
            self.statusBar().showMessage("Нет данных для отображения")
            return
        
        # Получаем значения фильтров
        status_filter = self.ui.status_combo.currentText() if self.ui.status_combo.isVisible() else "Все статусы"
        date_from = self.ui.date_from.date().toPyDate() if self.ui.date_from.isVisible() else None
        date_to = self.ui.date_to.date().toPyDate() if self.ui.date_to.isVisible() else None
        client_search = self.ui.client_search.text().strip().lower() if self.ui.client_search.isVisible() else ""
        
        filtered_orders = []
        
        for order in self._orders_cache:
            # Фильтр по статусу
            if status_filter != "Все статусы":
                if not order.status.lower() or order.status.name.lower() != status_filter:
                    continue
            
            # Фильтр по дате
            if date_from and order.order_date:
                if order.order_date < date_from:
                    continue
            if date_to and order.order_date:
                if order.order_date > date_to:
                    continue
            
            # Фильтр по клиенту
            if client_search:
                if not order.user or not order.user.full_name:
                    continue
                client_name = order.user.full_name.lower()
                
                # РАЗБИВАЕМ ПОИСК ПО СЛОВАМ
                search_words = client_search.split()
                client_words = client_name.split()
                
                # Проверяем, содержатся ли все слова поиска в любом порядке
                # Например: "Иван Петров" найдется в "Петров Иван Сергеевич"
                match_found = True
                for word in search_words:
                    if not any(word in client_word for client_word in client_words):
                        match_found = False
                        break
                
                if not match_found:
                    continue
            
            filtered_orders.append(order)
        
        # Сортируем по дате (новые сверху)
        filtered_orders.sort(key=lambda x: x.order_date if x.order_date else datetime.min, reverse=True)
        
        # Отображаем в таблице
        self.display_orders(filtered_orders)
    
    def display_orders(self, orders):
        """Отображение заказов в таблице"""
        self.ui.table.setRowCount(len(orders))
        
        for row, order in enumerate(orders):
            # ID
            id_item = QtWidgets.QTableWidgetItem(str(order.id))
            id_item.setFlags(id_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.ui.table.setItem(row, 0, id_item)
            
            # Дата заказа
            date_str = order.order_date.strftime("%d.%m.%Y") if order.order_date else ""
            date_item = QtWidgets.QTableWidgetItem(date_str)
            date_item.setFlags(date_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.ui.table.setItem(row, 1, date_item)
            
            # Клиент
            client_name = order.user.full_name if order.user else "Неизвестно"
            client_item = QtWidgets.QTableWidgetItem(client_name)
            client_item.setFlags(client_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.ui.table.setItem(row, 2, client_item)
            
            # Сумма заказа
            total = self.calculate_order_total(order)
            total_item = QtWidgets.QTableWidgetItem(f"{total:.2f} руб.")
            total_item.setFlags(total_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            total_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            self.ui.table.setItem(row, 3, total_item)
            
            # Статус
            status_name = order.status.name if order.status else "Без статуса"
            status_item = QtWidgets.QTableWidgetItem(status_name)
            status_item.setFlags(status_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            
            # Цвет статуса
            if order.status:
                if order.status.name == "Новый":
                    status_item.setBackground(QtGui.QColor("#FFE5B4"))  # светло-оранжевый
                elif order.status.name == "Обработан":
                    status_item.setBackground(QtGui.QColor("#ADD8E6"))  # светло-голубой
                elif order.status.name == "Доставляется":
                    status_item.setBackground(QtGui.QColor("#FFD700"))  # золотой
                elif order.status.name == "Готов к выдаче":
                    status_item.setBackground(QtGui.QColor("#90EE90"))  # светло-зеленый
                elif order.status.name == "Выдан":
                    status_item.setBackground(QtGui.QColor("#98FB98"))  # пастельно-зеленый
                elif order.status.name == "Завершен":
                    status_item.setBackground(QtGui.QColor("#98FB98"))  # пастельно-зеленый
                elif order.status.name == "Отменен":
                    status_item.setBackground(QtGui.QColor("#FFB6C1"))  # светло-розовый
            
            self.ui.table.setItem(row, 4, status_item)
            
            # Пункт выдачи
            pickup_info = ""
            if order.pickup_point:
                pickup_info = f"{order.pickup_point.city}, {order.pickup_point.street} {order.pickup_point.building}"
            pickup_item = QtWidgets.QTableWidgetItem(pickup_info)
            pickup_item.setFlags(pickup_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.ui.table.setItem(row, 5, pickup_item)
            
            # Код получения
            code_item = QtWidgets.QTableWidgetItem(order.pickup_code or "")
            code_item.setFlags(code_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.ui.table.setItem(row, 6, code_item)
            
            # Количество товаров
            items_count = len(order.details) if order.details else 0
            count_item = QtWidgets.QTableWidgetItem(str(items_count))
            count_item.setFlags(count_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            count_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.table.setItem(row, 7, count_item)
        
        # Показываем сообщение о количестве отфильтрованных заказов
        if len(orders) > 0:
            self.statusBar().showMessage(f"Показано {len(orders)} из {len(self._orders_cache)} заказов", 3000)
        
        self.ui.table.resizeRowsToContents()
        self.ui.table.horizontalHeader().setStretchLastSection(True)
    
    def calculate_order_total(self, order):
        """Вычисление общей суммы заказа"""
        total = 0.0
        if order.details:
            for detail in order.details:
                price = float(detail.price_at_order) if detail.price_at_order else 0.0
                total += (detail.quantity * price)
        return total
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.ui.status_combo.setCurrentIndex(0)
        self.ui.date_from.setDate(QtCore.QDate.currentDate().addMonths(-1))
        self.ui.date_to.setDate(QtCore.QDate.currentDate())
        self.ui.client_search.clear()
        self.apply_filters()
    
    def on_table_double_click(self, row, column):
        """Двойной клик по строке - просмотр деталей"""
        self.view_order_details()
    
    def view_order_details(self):
        """Просмотр деталей выбранного заказа"""
        selected_items = self.ui.table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.information(self, "Информация", "Выберите заказ для просмотра")
            return
        
        row = selected_items[0].row()
        order_id_item = self.ui.table.item(row, 0)
        if not order_id_item:
            return
        
        order_id = int(order_id_item.text())
        
        # Закрываем предыдущее окно, если открыто
        if self._details_window and self._details_window.isVisible():
            self._details_window.close()
        
        # Открываем новое окно с деталями
        try:
            self._details_window = OrderDetailsWindow(order_id, parent=self)
            self._details_window.show()
        except ImportError as e:
            QtWidgets.QMessageBox.warning(self, "Внимание", f"Окно деталей недоступно: {e}")
    
    def add_order(self):
        """Добавление нового заказа"""
        try:
            if self._edit_window and self._edit_window.isVisible():
                self._edit_window.close()
            
            self._edit_window = OrderEditWindow(parent=self)
            self._edit_window.saved.connect(self.refresh_orders)
            self._edit_window.show()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось открыть окно добавления заказа: {e}")
    
    def edit_order(self):
        """Редактирование выбранного заказа"""
        selected_items = self.ui.table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.information(self, "Информация", "Выберите заказ для редактирования")
            return
        
        row = selected_items[0].row()
        order_id_item = self.ui.table.item(row, 0)
        if not order_id_item:
            return
        
        order_id = int(order_id_item.text())
        
        try:
            if self._edit_window and self._edit_window.isVisible():
                self._edit_window.close()
            
            self._edit_window = OrderEditWindow(order_id=order_id, parent=self)
            self._edit_window.saved.connect(self.refresh_orders)
            self._edit_window.show()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось открыть окно редактирования заказа: {e}")
            
    def delete_selected_order(self):
        """Удаление заказа (только для администратора)"""
        if self.role_name != "Администратор":
            QtWidgets.QMessageBox.warning(self, "Доступ запрещен", 
                                        "Только администратор может удалять заказы")
            return
        
        selected_items = self.ui.table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.information(self, "Информация", "Выберите заказ для удаления")
            return
        
        row = selected_items[0].row()
        order_id_item = self.ui.table.item(row, 0)
        if not order_id_item:
            return
        
        order_id = int(order_id_item.text())
        
        # Подтверждение
        reply = QtWidgets.QMessageBox.question(
            self, "Подтверждение удаления",
            f"Вы уверены, что хотите удалить заказ #{order_id}?\nЭто действие нельзя отменить.",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                delete_order(order_id)
                QtWidgets.QMessageBox.information(self, "Успех", "Заказ удален")
                self.refresh_orders()  # Обновляем список заказов
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось удалить заказ: {e}")
    
    def go_back(self):
        """Возврат к предыдущему окну"""
        if self.parent_main:
            self.parent_main.show()
        self.close()
    
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        # Закрываем дочерние окна
        if self._details_window and self._details_window.isVisible():
            self._details_window.close()
        event.accept()