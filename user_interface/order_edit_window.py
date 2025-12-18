# user_interface/order_edit_window.py
import os
from datetime import datetime
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import pyqtSignal
from ui.ui_order_edit import Ui_OrderEditWindow

from crud.orders import create_order, get_order_by_id, update_order, create_order_detail
from crud.orders import get_all_orders  # для проверки
from crud.references import get_all_order_statuses, get_all_pickup_points, get_all_users
from crud.products import get_all_products

class OrderEditWindow(QtWidgets.QDialog):
    saved = pyqtSignal()

    def __init__(self, order_id=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_OrderEditWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.order_id = order_id
        self.order_details_data = []  # список товаров в заказе: [{"product_id": int, "quantity": int, "price": float}]
        
        # Подключение сигналов
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.ui.btn_add_product.clicked.connect(self.add_product_to_order)
        self.ui.btn_remove_product.clicked.connect(self.remove_selected_product)
        self.ui.cmb_product.currentIndexChanged.connect(self.on_product_selected)
        
        self._fill_refs()
        if self.order_id:
            self._load_order()
        else:
            # Для нового заказа устанавливаем текущую дату
            self.ui.date_order.setDate(QtCore.QDate.currentDate())
            self.ui.date_delivery.setDate(QtCore.QDate.currentDate().addDays(3))
            # Генерируем код получения
            self.generate_pickup_code()
    
    def _fill_refs(self):
        """Заполняем справочники"""
        # Пользователи
        self.ui.cmb_user.clear()
        users = get_all_users()
        self.ui.cmb_user.addItem("", None)
        for user in users:
            self.ui.cmb_user.addItem(user.full_name, user.id)
        
        # Статусы заказов
        self.ui.cmb_status.clear()
        statuses = get_all_order_statuses()
        self.ui.cmb_status.addItem("", None)
        for status in statuses:
            self.ui.cmb_status.addItem(status.name, status.id)
        
        # Пункты выдачи
        self.ui.cmb_pickup_point.clear()
        pickup_points = get_all_pickup_points()
        self.ui.cmb_pickup_point.addItem("", None)
        for pp in pickup_points:
            display_text = f"{pp.city}, {pp.street} {pp.building}"
            self.ui.cmb_pickup_point.addItem(display_text, pp.id)
        
        # Товары для добавления в заказ
        self.ui.cmb_product.clear()
        products = get_all_products()
        self.ui.cmb_product.addItem("Выберите товар", None)
        for product in products:
            display_text = f"{product.name} (Цена: {product.price} руб., Остаток: {product.quantity} шт.)"
            self.ui.cmb_product.addItem(display_text, product.id)
    
    def _load_order(self):
        """Загружаем существующий заказ"""
        order = get_order_by_id(self.order_id)
        if not order:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Заказ не найден")
            self.reject()
            return
        
        # Пользователь
        if order.user_id:
            idx = self.ui.cmb_user.findData(order.user_id)
            if idx != -1:
                self.ui.cmb_user.setCurrentIndex(idx)
        
        # Статус
        if order.status_id:
            idx = self.ui.cmb_status.findData(order.status_id)
            if idx != -1:
                self.ui.cmb_status.setCurrentIndex(idx)
        
        # Пункт выдачи
        if order.pickup_point_id:
            idx = self.ui.cmb_pickup_point.findData(order.pickup_point_id)
            if idx != -1:
                self.ui.cmb_pickup_point.setCurrentIndex(idx)
        
        # Даты
        if order.order_date:
            self.ui.date_order.setDate(QtCore.QDate(order.order_date))
        if order.delivery_date:
            self.ui.date_delivery.setDate(QtCore.QDate(order.delivery_date))
        
        # Код получения
        if order.pickup_code:
            self.ui.input_pickup_code.setText(order.pickup_code)
        
        # Загружаем товары заказа
        self.order_details_data = []
        if order.details:
            for detail in order.details:
                product_info = {
                    "product_id": detail.product_id,
                    "product_name": detail.product.name if detail.product else "Неизвестно",
                    "quantity": detail.quantity,
                    "price": float(detail.price_at_order) if detail.price_at_order else 0.0,
                    "total": detail.quantity * float(detail.price_at_order) if detail.price_at_order else 0.0
                }
                self.order_details_data.append(product_info)
        
        # Обновляем таблицу товаров
        self.update_products_table()
        self.update_total()
    
    def on_product_selected(self, index):
        """При выборе товара показываем его цену"""
        if index <= 0:
            self.ui.label_price.setText("Цена: -")
            self.ui.input_quantity.setValue(1)
            return
        
        product_id = self.ui.cmb_product.currentData()
        if product_id:
            products = get_all_products()
            for product in products:
                if product.id == product_id:
                    self.ui.label_price.setText(f"Цена: {product.price} руб.")
                    # Устанавливаем максимальное количество = остаток на складе
                    self.ui.input_quantity.setMaximum(product.quantity or 0)
                    break
    
    def add_product_to_order(self):
        """Добавляем товар в заказ"""
        product_id = self.ui.cmb_product.currentData()
        quantity = self.ui.input_quantity.value()
        
        if not product_id:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите товар")
            return
        
        if quantity <= 0:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Количество должно быть больше 0")
            return
        
        # Проверяем, не добавлен ли уже этот товар
        for item in self.order_details_data:
            if item["product_id"] == product_id:
                QtWidgets.QMessageBox.warning(self, "Предупреждение", "Этот товар уже добавлен в заказ")
                return
        
        # Получаем информацию о товаре
        products = get_all_products()
        product = None
        product_name = ""
        price = 0.0
        for p in products:
            if p.id == product_id:
                product = p
                product_name = p.name
                price = float(p.price) if p.price else 0.0
                break
        
        if not product:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Товар не найден")
            return
        
        # Проверяем остаток на складе
        if product.quantity and quantity > product.quantity:
            QtWidgets.QMessageBox.critical(self, "Ошибка", 
                                        f"Недостаточно товара на складе. Доступно: {product.quantity} шт.")
            return
        
        # Добавляем товар в список
        product_info = {
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "total": quantity * price
        }
        self.order_details_data.append(product_info)
        
        # Обновляем таблицу и общую сумму
        self.update_products_table()
        self.update_total()
        
        # Сбрасываем выбор товара
        self.ui.cmb_product.setCurrentIndex(0)
        self.ui.input_quantity.setValue(1)
    
    def remove_selected_product(self):
        """Удаляем выбранный товар из заказа"""
        selected_items = self.ui.table_products.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите товар для удаления")
            return
        
        row = selected_items[0].row()
        if 0 <= row < len(self.order_details_data):
            del self.order_details_data[row]
            self.update_products_table()
            self.update_total()
    
    def update_products_table(self):
        """Обновляем таблицу товаров в заказе"""
        self.ui.table_products.setRowCount(len(self.order_details_data))
        
        for row, item in enumerate(self.order_details_data):
            # Название товара
            name_item = QtWidgets.QTableWidgetItem(item["product_name"])
            name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.ui.table_products.setItem(row, 0, name_item)
            
            # Количество
            qty_item = QtWidgets.QTableWidgetItem(str(item["quantity"]))
            qty_item.setFlags(qty_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            qty_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.table_products.setItem(row, 1, qty_item)
            
            # Цена
            price_item = QtWidgets.QTableWidgetItem(f"{item['price']:.2f} руб.")
            price_item.setFlags(price_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            price_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            self.ui.table_products.setItem(row, 2, price_item)
            
            # Сумма
            total_item = QtWidgets.QTableWidgetItem(f"{item['total']:.2f} руб.")
            total_item.setFlags(total_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            total_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            self.ui.table_products.setItem(row, 3, total_item)
    
    def update_total(self):
        """Обновляем общую сумму заказа"""
        total = sum(item["total"] for item in self.order_details_data)
        self.ui.label_total.setText(f"Общая сумма: {total:.2f} руб.")
    
    def generate_pickup_code(self):
        """Генерируем случайный код получения"""
        import random
        import string
        code = ''.join(random.choices(string.digits, k=6))
        self.ui.input_pickup_code.setText(code)
    
    def save(self):
        """Сохраняем заказ"""
        # Проверяем обязательные поля
        user_id = self.ui.cmb_user.currentData()
        if not user_id:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите пользователя")
            return
        
        status_id = self.ui.cmb_status.currentData()
        if not status_id:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите статус заказа")
            return
        
        pickup_point_id = self.ui.cmb_pickup_point.currentData()
        if not pickup_point_id:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите пункт выдачи")
            return
        
        if not self.order_details_data:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Добавьте хотя бы один товар в заказ")
            return
        
        # Получаем данные
        order_date = self.ui.date_order.date().toPyDate()
        delivery_date = self.ui.date_delivery.date().toPyDate() if self.ui.date_delivery.date().isValid() else None
        pickup_code = self.ui.input_pickup_code.text().strip()
        
        try:
            if self.order_id:
                # Обновляем существующий заказ
                order = update_order(
                    self.order_id,
                    user_id=user_id,
                    status_id=status_id,
                    pickup_point_id=pickup_point_id,
                    order_date=order_date,
                    delivery_date=delivery_date,
                    pickup_code=pickup_code
                )
                
                # УДАЛЯЕМ старые товары и добавляем новые
                # В реальном приложении нужно сделать функцию для удаления старых деталей заказа
                # Пока что просто перезаписываем
                message = "Заказ обновлен"
            else:
                # Создаем новый заказ
                order = create_order(
                    user_id=user_id,
                    status_id=status_id,
                    pickup_point_id=pickup_point_id,
                    delivery_date=delivery_date,
                    pickup_code=pickup_code
                )
                
                # Обновляем дату заказа (она по умолчанию ставится текущая)
                if order_date != datetime.now().date():
                    update_order(order.id, order_date=order_date)
                
                message = "Заказ создан"
            
            # Добавляем/обновляем товары в заказе
            # В реальном приложении нужно удалить старые детали для редактирования
            for item in self.order_details_data:
                create_order_detail(
                    order_id=order.id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price_at_order=item["price"]
                )
            
            QtWidgets.QMessageBox.information(self, "Готово", message)
            self.saved.emit()
            self.accept()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить заказ: {str(e)}")