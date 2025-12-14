# user_interface/products_window.py
import os
from PyQt6 import QtWidgets, QtGui, QtCore
from ui.ui_products import Ui_ProductsWindow
from crud.products import get_all_products, delete_product
from crud.references import get_all_suppliers
from user_interface.product_edit_window import ProductEditWindow

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def images_full_path(filename):
    if not filename:
        return None
    return os.path.join(PROJECT_DIR, "images", filename)

class ProductsWindow(QtWidgets.QMainWindow):
    def __init__(self, user=None, parent_login=None):
        super().__init__()
        self.ui = Ui_ProductsWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        
        self.user = user
        self.parent_login = parent_login  # Ссылка на окно входа для возврата
        self._products_cache = []
        self._edit_window = None
        
        # Setup UI according to role
        role_name = user.role.name if user and user.role else "guest"
        self.role_name = role_name

        is_admin = role_name == "Администратор"
        is_manager = role_name == "Менеджер"

        # Показываем/скрываем элементы
        self.ui.search_input.setVisible(is_manager or is_admin)
        self.ui.supplier_filter.setVisible(is_manager or is_admin)
        self.ui.sort_box.setVisible(is_manager or is_admin)

        self.ui.btn_add.setVisible(is_admin)
        self.ui.btn_edit.setVisible(is_admin)
        self.ui.btn_delete.setVisible(is_admin)
        self.ui.btn_orders.setVisible(is_manager or is_admin)

        # Лейбл пользователя
        if user:
            self.ui.label_user.setText(f"{user.full_name} ({role_name})")
        else:
            self.ui.label_user.setText("Гость")

        # Connect signals
        self.ui.btn_back.clicked.connect(self.logout)
        self.ui.search_input.textChanged.connect(self.apply_filters)
        self.ui.supplier_filter.currentTextChanged.connect(self.apply_filters)
        self.ui.sort_box.currentTextChanged.connect(self.apply_filters)
        self.ui.btn_add.clicked.connect(self.handle_add)
        self.ui.btn_edit.clicked.connect(self.handle_edit)
        self.ui.btn_delete.clicked.connect(self.handle_delete)
        self.ui.btn_orders.clicked.connect(self.open_orders_window)
        
        # УДАЛЕНО: self.ui.table.cellDoubleClicked.connect(self.on_table_double_click)
        # Вместо этого отслеживаем выбор строки для активации кнопок
        self.ui.table.itemSelectionChanged.connect(self.on_selection_changed)

        # Fill supplier combo
        self._fill_suppliers()

        # Load products
        self.load_products()
        
        # Устанавливаем заголовок окна
        self.setWindowTitle("Каталог товаров")
        
        # Инициализируем состояние кнопок редактирования/удаления
        self.on_selection_changed()

    def _fill_suppliers(self):
        self.ui.supplier_filter.clear()
        self.ui.supplier_filter.addItem("Все поставщики")
        suppliers = get_all_suppliers()
        for s in suppliers:
            self.ui.supplier_filter.addItem(s.name)

    def load_products(self):
        products = get_all_products()
        self._products_cache = products
        self.apply_filters()

    def apply_filters(self):
        q = self.ui.search_input.text().strip().lower() if self.ui.search_input.isVisible() else ""
        supplier = self.ui.supplier_filter.currentText() if self.ui.supplier_filter.isVisible() else "Все поставщики"
        sort_sel = self.ui.sort_box.currentText() if self.ui.sort_box.isVisible() else "Нет сортировки"
        if not self._products_cache:
            self.ui.table.setRowCount(0)
            return

        filtered = []
        for p in self._products_cache:
            # Guest/client: no search/filter applied per spec
            if not (self.ui.search_input.isVisible()):
                filtered.append(p)
                continue

            # search across text fields (name, description, manufacturer, supplier, category)
            match = True
            if q:
                qmatch = False
                fields = [
                    p.name or "",
                    p.description or "",
                    (p.manufacturer.name if p.manufacturer else "") or "",
                    (p.supplier.name if p.supplier else "") or "",
                    (p.category.name if p.category else "") or ""
                ]
                for f in fields:
                    if q in f.lower():
                        qmatch = True
                        break
                if not qmatch:
                    match = False

            if supplier and supplier != "Все поставщики":
                if not p.supplier or p.supplier.name != supplier:
                    match = False

            if match:
                filtered.append(p)

        # Sorting by quantity
        if sort_sel == "Кол-во ↑":
            filtered.sort(key=lambda x: (x.quantity or 0))
        elif sort_sel == "Кол-во ↓":
            filtered.sort(key=lambda x: (x.quantity or 0), reverse=True)

        self.display_products(filtered)

    def display_products(self, products):
        table = self.ui.table
        table.clearContents()
        table.setRowCount(len(products))

        for row, p in enumerate(products):
            # ID column (hidden in UI but we need it)
            id_item = QtWidgets.QTableWidgetItem(str(p.id))
            id_item.setFlags(id_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)  # Делаем нередактируемым
            table.setItem(row, 0, id_item)
            
            # Name, Category, Description, Manufacturer, Supplier
            name_item = QtWidgets.QTableWidgetItem(p.name)
            name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 1, name_item)
            
            category_name = p.category.name if (p.category and hasattr(p.category, 'name')) else ""
            category_item = QtWidgets.QTableWidgetItem(category_name)
            category_item.setFlags(category_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 2, category_item)
            
            desc_item = QtWidgets.QTableWidgetItem(p.description or "")
            desc_item.setFlags(desc_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 3, desc_item)
            
            manuf_item = QtWidgets.QTableWidgetItem(p.manufacturer.name if p.manufacturer else "")
            manuf_item.setFlags(manuf_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 4, manuf_item)
            
            supp_item = QtWidgets.QTableWidgetItem(p.supplier.name if p.supplier else "")
            supp_item.setFlags(supp_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 5, supp_item)

            # Price display with discount
            base_price = float(p.price) if p.price else 0.00
            discount = float(p.discount) if p.discount else 0.0

            # Определяем фон строки
            bg_color = None
            if p.discount and discount > 15:
                bg_color = QtGui.QColor("#2E8B57")
            elif (p.quantity or 0) == 0:
                bg_color = QtGui.QColor("#ADD8E6")

            if discount > 0:
                final_price = base_price * (1 - discount / 100)

                # Оригинальная цена — красная, зачёркнутая
                original_label = QtWidgets.QLabel(f"{base_price:.2f}")
                original_font = QtGui.QFont("Times New Roman", 8)
                original_font.setStrikeOut(True)
                original_label.setFont(original_font)
                original_label.setStyleSheet("color: red;")
                original_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

                # Цена со скидкой — чёрная, обычная
                final_label = QtWidgets.QLabel(f"{final_price:.2f}")
                final_label.setFont(QtGui.QFont("Times New Roman", 8))
                final_label.setStyleSheet("color: black;")
                final_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

                # Компоновка
                layout = QtWidgets.QHBoxLayout()
                layout.setContentsMargins(2, 0, 2, 0)
                layout.addWidget(original_label)
                layout.addWidget(final_label)
                layout.addStretch()

                container = QtWidgets.QWidget()
                container.setLayout(layout)
                container.setAutoFillBackground(False)

                table.setCellWidget(row, 6, container)
            else:
                # Нет скидки — просто обычная цена
                price_label = QtWidgets.QLabel(f"{base_price:.2f}")
                price_label.setFont(QtGui.QFont("Times New Roman", 8))
                price_label.setStyleSheet("color: black;")
                price_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
                price_label.setAutoFillBackground(False)

                table.setCellWidget(row, 6, price_label)

            # Discount column
            discount_item = QtWidgets.QTableWidgetItem(f"{discount:.2f}%" if p.discount else "0.00%")
            discount_item.setFlags(discount_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 7, discount_item)
            
            quantity_item = QtWidgets.QTableWidgetItem(str(p.quantity or 0))
            quantity_item.setFlags(quantity_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 8, quantity_item)

            # Photo
            photo_label = QtWidgets.QLabel()
            photo_label.setFixedSize(100, 60)

            img_path = None
            if p.image_path:
                candidate = images_full_path(p.image_path)
                if candidate and os.path.exists(candidate):
                    img_path = candidate

            # fallback: всегда использовать заглушку images/Icon.png
            if not img_path:
                placeholder = os.path.join(PROJECT_DIR, "images", "Icon.JPG")
                img_path = placeholder if os.path.exists(placeholder) else None

            if img_path:
                pix = QtGui.QPixmap(img_path)
                if pix.isNull() and os.path.exists(placeholder):
                    pix = QtGui.QPixmap(placeholder)
                photo_label.setPixmap(pix.scaled(photo_label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio))

            table.setCellWidget(row, 9, photo_label)

            # Применяем фон ко всем ячейкам строки
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    if bg_color:
                        item.setBackground(bg_color)
                    else:
                        item.setBackground(QtGui.QColor("white"))

        table.resizeRowsToContents()

    def on_selection_changed(self):
        """Активирует/деактивирует кнопки редактирования и удаления в зависимости от выбора"""
        has_selection = len(self.ui.table.selectedItems()) > 0
        
        # Включаем кнопки только если есть выделение и пользователь администратор
        if has_selection and self.role_name == "Администратор":
            self.ui.btn_edit.setEnabled(True)
            self.ui.btn_delete.setEnabled(True)
        else:
            self.ui.btn_edit.setEnabled(False)
            self.ui.btn_delete.setEnabled(False)

    def handle_add(self):
        if self._edit_window and self._edit_window.isVisible():
            QtWidgets.QMessageBox.warning(self, "Внимание", "Окно добавления/редактирования уже открыто")
            return
        try:
            self._edit_window = ProductEditWindow(parent=self)
            self._edit_window.saved.connect(self.on_edit_saved)
            self._edit_window.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось открыть окно редактирования: {str(e)}")
            print(f"Error opening edit window: {e}")  # Для отладки

    def handle_edit(self):
        # Получаем выделенную строку
        selected_rows = set()
        for item in self.ui.table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QtWidgets.QMessageBox.information(self, "Информация", "Выберите товар для редактирования")
            return
        
        # Берем первую выделенную строку
        row = list(selected_rows)[0]
        item = self.ui.table.item(row, 0)
        if not item:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось получить ID товара")
            return
        
        try:
            pid = int(item.text())
            self.open_edit(pid)
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Неверный ID товара: {str(e)}")
            print(f"Error parsing product ID: {e}")

    def open_edit(self, product_id: int):
        if self._edit_window and self._edit_window.isVisible():
            QtWidgets.QMessageBox.warning(self, "Внимание", "Окно добавления/редактирования уже открыто")
            return
        
        try:
            self._edit_window = ProductEditWindow(product_id=product_id, parent=self)
            self._edit_window.saved.connect(self.on_edit_saved)
            self._edit_window.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось открыть окно редактирования: {str(e)}")
            print(f"Error opening edit window for product {product_id}: {e}")  # Для отладки

    def on_edit_saved(self):
        # refresh products
        self.load_products()

    def handle_delete(self):
        # Получаем выделенную строку
        selected_rows = set()
        for item in self.ui.table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QtWidgets.QMessageBox.information(self, "Информация", "Выберите товар для удаления")
            return
        
        # Берем первую выделенную строку
        row = list(selected_rows)[0]
        item = self.ui.table.item(row, 0)
        if not item:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось получить ID товара")
            return
        
        try:
            pid = int(item.text())
            
            # Получаем название товара для подтверждения
            name_item = self.ui.table.item(row, 1)
            product_name = name_item.text() if name_item else f"ID: {pid}"
            
            # confirm
            reply = QtWidgets.QMessageBox.question(
                self, 
                "Подтверждение удаления", 
                f"Вы уверены, что хотите удалить товар \"{product_name}\"?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )
            
            if reply != QtWidgets.QMessageBox.StandardButton.Yes:
                return
            
            delete_product(pid)
            QtWidgets.QMessageBox.information(self, "Успех", f"Товар \"{product_name}\" успешно удалён")
            self.load_products()
            
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Неверный ID товара: {str(e)}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось удалить товар: {str(e)}")
            print(f"Error deleting product: {e}")  # Для отладки
        
    def open_orders_window(self):
        """Открывает окно управления заказами"""
        try:
            from user_interface.orders_window import OrdersWindow
            self.orders_window = OrdersWindow(user=self.user, parent_main=self)
            self.orders_window.show()
            self.hide()  # Скрываем текущее окно
        except ImportError as e:
            QtWidgets.QMessageBox.warning(self, "Внимание", f"Окно заказов недоступно: {e}")

    def logout(self):
        """Выход из системы - возврат к окну входа"""
        if self.parent_login:
            # Показываем окно входа
            self.parent_login.show()
        
        # Закрываем текущее окно
        self.close()
        
        # Если нет ссылки на окно входа, создаем новое
        if not self.parent_login:
            from user_interface.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()

    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        # Если окно закрывается (крестик), показываем окно входа
        if not self.parent_login:
            from user_interface.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
        event.accept()