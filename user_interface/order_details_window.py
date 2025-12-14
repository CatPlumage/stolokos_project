from PyQt6 import QtWidgets, QtGui, QtCore
from decimal import Decimal
from ui.ui_order_details import Ui_OrderDetailsWindow
from crud.orders import get_order_by_id


class OrderDetailsWindow(QtWidgets.QMainWindow):
    def __init__(self, order_id: int, parent=None):
        super().__init__(parent)
        self.order_id = order_id
        self.order = None
        
        # Инициализация UI
        self.ui = Ui_OrderDetailsWindow()
        self.ui.setupUi(self)
        
        # Настройка заголовка окна
        self.setWindowTitle(f"Детали заказа #{self.order_id}")
        
        # Подключение сигналов
        self.ui.btn_close.clicked.connect(self.close)
        
        # Загрузка данных
        self.load_order_details()
        
    def load_order_details(self):
        """Загружаем детали заказа"""
        try:
            # Получаем заказ с связанными данными
            self.order = get_order_by_id(self.order_id)
            
            if not self.order:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Заказ не найден")
                self.close()
                return
            
            # Заполняем информацию о заказе
            self.ui.labels["id"].setText(str(self.order.id))
            
            if self.order.order_date:
                self.ui.labels["order_date"].setText(self.order.order_date.strftime("%d.%m.%Y"))
            else:
                self.ui.labels["order_date"].setText("Не указана")
            
            if self.order.user:
                self.ui.labels["client"].setText(self.order.user.full_name)
            else:
                self.ui.labels["client"].setText("Неизвестно")
            
            if self.order.status:
                self.ui.labels["status"].setText(self.order.status.name)
                # Устанавливаем цвет статуса
                self._set_status_color(self.order.status.name)
            else:
                self.ui.labels["status"].setText("Без статуса")
            
            if self.order.pickup_point:
                self.ui.labels["pickup_point"].setText(
                    f"{self.order.pickup_point.city}, {self.order.pickup_point.street}"
                )
                self.ui.labels["address"].setText(
                    f"{self.order.pickup_point.street} {self.order.pickup_point.building}"
                )
            else:
                self.ui.labels["pickup_point"].setText("Не указан")
                self.ui.labels["address"].setText("Не указан")
            
            self.ui.labels["pickup_code"].setText(self.order.pickup_code or "Не указан")
            
            if self.order.delivery_date:
                self.ui.labels["delivery_date"].setText(
                    self.order.delivery_date.strftime("%d.%m.%Y")
                )
            else:
                self.ui.labels["delivery_date"].setText("Не указана")
            
            # Заполняем таблицу товаров
            self.load_products_table()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить детали заказа: {str(e)}")
            import traceback
            traceback.print_exc()
            self.close()
    
    def _set_status_color(self, status_name):
        """Устанавливает цвет фона для статуса"""
        colors = {
            "Новый": "#FFE5B4",          # светло-оранжевый
            "Обработан": "#ADD8E6",      # светло-голубой
            "Доставляется": "#FFD700",   # золотой
            "Готов к выдаче": "#90EE90", # светло-зеленый
            "Выдан": "#98FB98",          # пастельно-зеленый
            "Завершен": "#98FB98",       # пастельно-зеленый
            "Отменен": "#FFB6C1"         # светло-розовый
        }
        
        color = colors.get(status_name, "#FFFFFF")
        self.ui.labels["status"].setStyleSheet(f"background-color: {color}; padding: 3px; border: 1px solid #E0E0E0; border-radius: 3px;")
    
    def load_products_table(self):
        """Заполняем таблицу товарами заказа"""
        if not self.order or not self.order.details:
            self.ui.products_table.setRowCount(0)
            self.ui.labels["total_amount"].setText("0.00 руб.")
            self.ui.total_label.setText("Итого к оплате: 0.00 руб.")
            return
        
        self.ui.products_table.setRowCount(len(self.order.details))
        
        total_amount = Decimal('0.0')
        
        for row, detail in enumerate(self.order.details):
            product = detail.product
            
            # Название товара
            name_item = QtWidgets.QTableWidgetItem(product.name if product else "Товар удален")
            name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.ui.products_table.setItem(row, 0, name_item)
            
            # Артикул
            article_item = QtWidgets.QTableWidgetItem(product.article if product and product.article else "")
            article_item.setFlags(article_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            article_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.products_table.setItem(row, 1, article_item)
            
            # Количество
            quantity_item = QtWidgets.QTableWidgetItem(str(detail.quantity))
            quantity_item.setFlags(quantity_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            quantity_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.products_table.setItem(row, 2, quantity_item)
            
            # Цена - безопасно конвертируем Decimal в float для отображения
            price_value = detail.price_at_order if detail.price_at_order else Decimal('0.0')
            try:
                price_float = float(price_value)
                price_item = QtWidgets.QTableWidgetItem(f"{price_float:.2f} руб.")
            except (TypeError, ValueError):
                price_item = QtWidgets.QTableWidgetItem("0.00 руб.")
            
            price_item.setFlags(price_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            price_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            self.ui.products_table.setItem(row, 3, price_item)
            
            # Скидка (если товар имеет скидку)
            if product and hasattr(product, 'discount'):
                discount_value = product.discount if product.discount else Decimal('0.0')
                try:
                    discount_float = float(discount_value)
                    discount_text = f"{discount_float:.1f}%" if discount_float > 0 else "0%"
                except (TypeError, ValueError):
                    discount_text = "0%"
            else:
                discount_text = "0%"
            
            discount_item = QtWidgets.QTableWidgetItem(discount_text)
            discount_item.setFlags(discount_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            discount_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.products_table.setItem(row, 4, discount_item)
            
            # Сумма - вычисляем с использованием Decimal, затем конвертируем в float
            try:
                quantity_decimal = Decimal(str(detail.quantity))
                price_decimal = detail.price_at_order if detail.price_at_order else Decimal('0.0')
                amount_decimal = quantity_decimal * price_decimal
                total_amount += amount_decimal
                
                amount_float = float(amount_decimal)
                amount_item = QtWidgets.QTableWidgetItem(f"{amount_float:.2f} руб.")
            except (TypeError, ValueError):
                amount_item = QtWidgets.QTableWidgetItem("0.00 руб.")
            
            amount_item.setFlags(amount_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            amount_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            self.ui.products_table.setItem(row, 5, amount_item)
        
        # Обновляем итоговую сумму
        try:
            total_float = float(total_amount)
            self.ui.labels["total_amount"].setText(f"{total_float:.2f} руб.")
            self.ui.total_label.setText(f"Итого к оплате: {total_float:.2f} руб.")
        except (TypeError, ValueError):
            self.ui.labels["total_amount"].setText("0.00 руб.")
            self.ui.total_label.setText("Итого к оплате: 0.00 руб.")
        
        # Устанавливаем высоту строк
        self.ui.products_table.resizeRowsToContents()
        
        # Делаем последнюю колонку растягиваемой
        self.ui.products_table.horizontalHeader().setStretchLastSection(True)