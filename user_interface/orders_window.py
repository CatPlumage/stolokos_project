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
        self._selected_card = None  # Для хранения выбранной карточки
        
        # Настройка прав доступа
        self.setup_role_permissions()
        
        # Загрузка заказов
        self.load_orders()
        
        # Подключение сигналов
        self.setup_connections()
        
        # Инициализируем состояние кнопок
        self.update_buttons_state()
        
    def setup_connections(self):
        """Подключение всех сигналов"""
        self.ui.btn_back.clicked.connect(self.go_back)
        self.ui.btn_apply.clicked.connect(self.apply_filters)
        self.ui.btn_reset.clicked.connect(self.reset_filters)
        self.ui.btn_refresh.clicked.connect(self.refresh_orders)
        self.ui.btn_add.clicked.connect(self.add_order)
        self.ui.btn_view_details.clicked.connect(self.view_order_details)
        self.ui.btn_delete.clicked.connect(self.delete_selected_order)
        # Убрали двойной клик по таблице
        
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
        self.ui.filter_group.setVisible(is_manager or is_admin)
        
        # Кнопки действий
        self.ui.btn_add.setVisible(is_admin)
        self.ui.btn_delete.setVisible(is_admin)
        
        # Если клиент, показываем только его заказы
        self.show_only_user_orders = is_client
    
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
            self.clear_cards()
            self.statusBar().showMessage("Нет данных для отображения")
            return
        
        # Получаем значение фильтра по клиенту
        client_search = self.ui.client_search.text().strip().lower() if self.ui.client_search.isVisible() else ""
        
        filtered_orders = []
        
        for order in self._orders_cache:
            # Фильтр по клиенту
            if client_search:
                if not order.user or not order.user.full_name:
                    continue
                client_name = order.user.full_name.lower()
                
                # РАЗБИВАЕМ ПОИСК ПО СЛОВАМ
                search_words = client_search.split()
                client_words = client_name.split()
                
                # Проверяем, содержатся ли все слова поиска в любом порядке
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
        
        # Отображаем в виде карточек
        self.display_orders(filtered_orders)
    
    def clear_cards(self):
        """Очищает все карточки заказов"""
        while self.ui.cards_layout.count():
            item = self.ui.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._selected_card = None
        self.update_buttons_state()
    
    def display_orders(self, orders):
        """Отображение заказов в виде карточек"""
        self.clear_cards()
        
        if not orders:
            # Показываем сообщение, если заказов нет
            no_orders_label = QtWidgets.QLabel("Заказы не найдены")
            no_orders_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            no_orders_label.setStyleSheet("font-size: 14pt; color: #666666; padding: 50px;")
            self.ui.cards_layout.addWidget(no_orders_label)
            return
        
        for order in orders:
            card = self.create_order_card(order)
            self.ui.cards_layout.addWidget(card)
        
        # Показываем сообщение о количестве отфильтрованных заказов
        if len(orders) > 0:
            self.statusBar().showMessage(f"Показано {len(orders)} из {len(self._orders_cache)} заказов", 3000)
    
    def create_order_card(self, order):
        """Создает карточку заказа"""
        card_widget = QtWidgets.QWidget()
        card_widget.setObjectName("card_widget")
        card_widget.setMinimumHeight(120)
        card_widget.setMaximumHeight(120)
        card_widget.setProperty("order_id", order.id)  # Сохраняем ID заказа
        card_widget.setProperty("original_style", "")  # Для хранения оригинального стиля
        
        # Определяем цвет статуса
        status_color = self.get_status_color(order.status.name if order.status else "Без статуса")
        
        # Оригинальный стиль карточки
        original_style = f"""
            background-color: white;
            border: 1px solid #FFFFFF;
            border-radius: 8px;
        """
        card_widget.setProperty("original_style", original_style)
        card_widget.setStyleSheet(original_style)
        
        # Основной layout карточки
        main_layout = QtWidgets.QHBoxLayout(card_widget)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(20)
        
        # Левая часть - основная информация
        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)
        
        # Заголовок с ID и датой
        title_widget = QtWidgets.QWidget()
        title_layout = QtWidgets.QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        
        # ID заказа
        order_id_label = QtWidgets.QLabel(f"Заказ #{order.id}")
        order_id_label.setStyleSheet("font-weight: bold; font-size: 11pt; color: #2E4A8C;")
        title_layout.addWidget(order_id_label)
        
        # Дата заказа
        date_str = order.order_date.strftime("%d.%m.%Y") if order.order_date else "Дата не указана"
        date_label = QtWidgets.QLabel(f"{date_str}")
        date_label.setStyleSheet("color: #666666;")
        title_layout.addWidget(date_label)
        
        title_layout.addStretch()
        
        left_layout.addWidget(title_widget)
        
        # Информация о клиенте
        client_name = order.user.full_name if order.user else "Неизвестный клиент"
        client_label = QtWidgets.QLabel(f"Клиент: {client_name}")
        client_label.setStyleSheet("font-size: 9pt;")
        left_layout.addWidget(client_label)
        
        # Пункт выдачи
        pickup_info = ""
        if order.pickup_point:
            pickup_info = f"{order.pickup_point.city}, {order.pickup_point.street} {order.pickup_point.building}"
        else:
            pickup_info = "Пункт выдачи не указан"
        pickup_label = QtWidgets.QLabel(pickup_info)
        pickup_label.setStyleSheet("font-size: 9pt;")
        left_layout.addWidget(pickup_label)
        
        left_layout.addStretch()
        
        main_layout.addWidget(left_widget, 6)  # 6 частей из 10
        
        # Правая часть - детали заказа
        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)
        
        # Сумма заказа
        total = self.calculate_order_total(order)
        total_label = QtWidgets.QLabel(f"{total:.2f} ₽")
        total_label.setStyleSheet("font-weight: bold; font-size: 11pt; color: #2E8B57;")
        right_layout.addWidget(total_label)
        
        # Количество товаров
        items_count = len(order.details) if order.details else 0
        items_label = QtWidgets.QLabel(f"Товаров: {items_count}")
        items_label.setStyleSheet("font-size: 9pt;")
        right_layout.addWidget(items_label)
        
        # Код получения
        code_text = f"Код: {order.pickup_code}" if order.pickup_code else "Код не указан"
        code_label = QtWidgets.QLabel(code_text)
        code_label.setStyleSheet("font-size: 9pt;")
        right_layout.addWidget(code_label)
        
        right_layout.addStretch()
        
        main_layout.addWidget(right_widget, 3)  # 3 части из 10
        
        # Крайняя правая часть - статус
        status_widget = QtWidgets.QWidget()
        status_widget.setFixedWidth(150)
        status_layout = QtWidgets.QVBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(5)
        
        # Статус заказа
        status_name = order.status.name if order.status else "Без статуса"
        status_label = QtWidgets.QLabel(status_name)
        status_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet(f"""
            font-weight: bold;
            font-size: 10pt;
            color: white;
            background-color: {status_color};
            border-radius: 12px;
            padding: 4px 8px;
        """)
        status_layout.addWidget(status_label)
        
        # Пустое пространство
        status_layout.addStretch()
        
        main_layout.addWidget(status_widget, 1)  # 1 часть из 10
        
        # Событие клика для выбора карточки
        card_widget.mousePressEvent = lambda e, card=card_widget: self.handle_card_click(e, card)
        
        return card_widget
    
    def handle_card_click(self, event, card):
        """Обработчик кликов по карточке"""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # Одинарный клик - выделение карточки
            self.select_card(card)
            
            # Если двойной клик - редактирование (только для администратора)
            if event.type() == QtCore.QEvent.Type.MouseButtonDblClick and self.role_name == "Администратор":
                self.handle_card_double_click(card)
    
    def handle_card_double_click(self, card):
        """Редактирование заказа по двойному клику"""
        if not card:
            return
        
        try:
            order_id = card.property("order_id")
            if order_id:
                self.edit_order(order_id)
        except (ValueError, AttributeError) as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось получить ID заказа: {str(e)}")
            print(f"Error parsing order ID: {e}")
    
    def get_status_color(self, status_name):
        """Возвращает цвет для статуса заказа"""
        color_map = {
            "Без статуса": "#808080"
        }
        return color_map.get(status_name, "#808080")
    
    def calculate_order_total(self, order):
        """Вычисление общей суммы заказа"""
        total = 0.0
        if order.details:
            for detail in order.details:
                price = float(detail.price_at_order) if detail.price_at_order else 0.0
                total += (detail.quantity * price)
        return total
    
    def select_card(self, card):
        """Выделяет карточку (меняет фон на акцентный) и снимает выделение с других"""
        # Снимаем выделение с предыдущей карточки (восстанавливаем оригинальный стиль)
        if self._selected_card:
            original_style = self._selected_card.property("original_style")
            self._selected_card.setStyleSheet(original_style)
        
        # Выделяем новую карточку - меняем фон на акцентный цвет
        selected_style = """
            background-color: #00FA9A;
            border: 1px solid #00FA9A;
            border-radius: 8px;
        """
        card.setStyleSheet(selected_style)
        
        self._selected_card = card
        self.update_buttons_state()
    
    def update_buttons_state(self):
        """Активирует/деактивирует кнопки действий"""
        has_selection = self._selected_card is not None
        
        # Кнопка удаления доступна только администраторам
        if has_selection and self.role_name == "Администратор":
            self.ui.btn_delete.setEnabled(True)
        else:
            self.ui.btn_delete.setEnabled(False)
        
        # Кнопка просмотра деталей доступна всем при наличии выбора
        if has_selection:
            self.ui.btn_view_details.setEnabled(True)
        else:
            self.ui.btn_view_details.setEnabled(False)
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.ui.client_search.clear()
        self.apply_filters()
    
    def view_order_details(self):
        """Просмотр деталей выбранного заказа"""
        if not self._selected_card:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите заказ для просмотра")
            return
        
        try:
            order_id = self._selected_card.property("order_id")
            
            # Закрываем предыдущее окно, если открыто
            if self._details_window and self._details_window.isVisible():
                self._details_window.close()
            
            # Открываем новое окно с деталями
            self._details_window = OrderDetailsWindow(order_id, parent=self)
            self._details_window.show()
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", f"Окно деталей недоступно: {e}")
    
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
    
    def edit_order(self, order_id=None):
        """Редактирование заказа (вызывается по двойному клику или с ID)"""
        if not order_id:
            # Если ID не передан, используем выделенный заказ
            if not self._selected_card:
                QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите заказ для редактирования")
                return
            order_id = self._selected_card.property("order_id")
        
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
        
        if not self._selected_card:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите заказ для удаления")
            return
        
        try:
            order_id = self._selected_card.property("order_id")
            
            # Подтверждение
            reply = QtWidgets.QMessageBox.question(
                self, "Подтверждение удаления",
                f"Вы уверены, что хотите удалить заказ #{order_id}?\nЭто действие нельзя отменить.",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
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