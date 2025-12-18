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
        self._selected_card = None  # Для хранения выбранной карточки
        
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

        # Fill supplier combo
        self._fill_suppliers()

        # Load products
        self.load_products()
        
        # Устанавливаем заголовок окна
        self.setWindowTitle("Каталог товаров")
        
        # Инициализируем состояние кнопок редактирования/удаления
        self.update_buttons_state()

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
            self.clear_cards()
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

    def clear_cards(self):
        # Удаляем все карточки
        while self.ui.cards_layout.count():
            item = self.ui.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._selected_card = None
        self.update_buttons_state()

    def display_products(self, products):
        self.clear_cards()
        
        if not products:
            # Показываем сообщение, если товаров нет
            no_products_label = QtWidgets.QLabel("Товары не найдены")
            no_products_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            no_products_label.setStyleSheet("font-size: 14pt; color: #666666; padding: 50px;")
            self.ui.cards_layout.addWidget(no_products_label)
            return
        
        for p in products:
            card = self.create_product_card(p)
            self.ui.cards_layout.addWidget(card)

    # user_interface/products_window.py (обновленный метод create_product_card)
    def create_product_card(self, product):
        """Создает карточку товара с фото слева и информацией справа"""
        card_widget = QtWidgets.QWidget()
        card_widget.setObjectName("card_widget")
        card_widget.setMinimumHeight(140)
        card_widget.setMaximumHeight(140)
        card_widget.setProperty("product_id", product.id)  # Сохраняем ID товара
        card_widget.setProperty("original_style", "")  # Для хранения оригинального стиля
        
        # Определяем оригинальный фон карточки
        original_bg_color = None
        if product.discount and float(product.discount) > 15:
            original_bg_color = "#2E8B57"  # Зеленый для большой скидки
        elif (product.quantity or 0) == 0:
            original_bg_color = "#ADD8E6"  # Голубой для нулевого количества
        else:
            original_bg_color = "#FFFFFF"  # Белый для остальных
        
        # Сохраняем оригинальный стиль в свойстве
        original_style = f"""
            background-color: {original_bg_color};
            border: 1px solid #FFFFFF;
            border-radius: 8px;
        """
        card_widget.setProperty("original_style", original_style)
        card_widget.setStyleSheet(original_style)
        
        # Основной layout карточки
        main_layout = QtWidgets.QHBoxLayout(card_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Левая часть - фото
        photo_frame = QtWidgets.QFrame()
        photo_frame.setFixedSize(120, 100)
        photo_frame.setStyleSheet("border: 1px solid #FFFFFF; background-color: white;")
        
        photo_layout = QtWidgets.QVBoxLayout(photo_frame)
        photo_layout.setContentsMargins(2, 2, 2, 2)
        photo_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # Загружаем фото
        photo_label = QtWidgets.QLabel()
        photo_label.setFixedSize(116, 96)
        photo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        img_path = None
        if product.image_path:
            candidate = images_full_path(product.image_path)
            if candidate and os.path.exists(candidate):
                img_path = candidate
        
        # fallback: всегда использовать заглушку images/Icon.png
        if not img_path:
            placeholder = os.path.join(PROJECT_DIR, "images", "Icon.JPG")
            img_path = placeholder if os.path.exists(placeholder) else None
        
        if img_path:
            pix = QtGui.QPixmap(img_path)
            if not pix.isNull():
                scaled_pix = pix.scaled(photo_label.size(), 
                                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                    QtCore.Qt.TransformationMode.SmoothTransformation)
                photo_label.setPixmap(scaled_pix)
            else:
                # Если изображение не загрузилось, показываем текст
                photo_label.setText("🖼️ Нет фото")
                photo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        photo_layout.addWidget(photo_label)
        
        # Правая часть - информация
        info_widget = QtWidgets.QWidget()
        info_layout = QtWidgets.QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)
        
        # Название товара
        name_label = QtWidgets.QLabel(f"🏷️ {product.name or 'Без названия'}")
        name_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        info_layout.addWidget(name_label)
        
        # Основная информация в две колонки
        details_widget = QtWidgets.QWidget()
        details_layout = QtWidgets.QHBoxLayout(details_widget)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(20)
        
        # Левая колонка с деталями
        left_details = QtWidgets.QVBoxLayout()
        left_details.setSpacing(3)
        
        # Категория
        if product.category and hasattr(product.category, 'name'):
            category_label = QtWidgets.QLabel(f"📂 {product.category.name}")
            left_details.addWidget(category_label)
        
        # Производитель
        if product.manufacturer:
            manufacturer_label = QtWidgets.QLabel(f"🏭 {product.manufacturer.name}")
            left_details.addWidget(manufacturer_label)
        
        # Поставщик
        if product.supplier:
            supplier_label = QtWidgets.QLabel(f"🚚 {product.supplier.name}")
            left_details.addWidget(supplier_label)
        
        details_layout.addLayout(left_details)
        
        # Правая колонка с ценой и количеством
        right_details = QtWidgets.QVBoxLayout()
        right_details.setSpacing(3)
        
        # Цена
        base_price = float(product.price) if product.price else 0.00
        discount = float(product.discount) if product.discount else 0.0
        
        if discount > 0:
            final_price = base_price * (1 - discount / 100)
            price_text = f"""
                <div style='font-size: 8pt; color: #666666;'>
                    💰 Цена:
                </div>
                <div style='text-decoration: line-through; color: red; font-size: 8pt;'>
                    {base_price:.2f} ₽
                </div>
                <div style='color: black; font-size: 10pt; font-weight: bold;'>
                    {final_price:.2f} ₽
                </div>
            """
        else:
            price_text = f"""
                <div style='font-size: 8pt; color: #666666;'>
                    💰 Цена:
                </div>
                <div style='font-size: 10pt; font-weight: bold;'>
                    {base_price:.2f} ₽
                </div>
            """
        
        price_label = QtWidgets.QLabel(price_text)
        price_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        right_details.addWidget(price_label)
        
        # Скидка
        if discount > 0:
            discount_color = "#FF0000"  # Красный для скидки
            if discount > 15:
                discount_color = "#2E8B57"  # Зеленый для большой скидки
            discount_label = QtWidgets.QLabel(f"🎯 {discount:.1f}%")
            discount_label.setStyleSheet(f"color: {discount_color}; font-weight: bold;")
            right_details.addWidget(discount_label)
        
        # Количество
        quantity = product.quantity or 0
        quantity_emoji = "📦"
        if quantity == 0:
            quantity_emoji = "⛔"
            quantity_label = QtWidgets.QLabel(f"{quantity_emoji} {quantity}")
            quantity_label.setStyleSheet("color: #0000FF; font-weight: bold;")
        else:
            quantity_label = QtWidgets.QLabel(f"{quantity_emoji} {quantity}")
            quantity_label.setStyleSheet("color: #2E8B57; font-weight: bold;")
        
        right_details.addWidget(quantity_label)
        
        details_layout.addLayout(right_details)
        info_layout.addWidget(details_widget)
        
        # Описание (если есть)
        if product.description:
            description_label = QtWidgets.QLabel(f"📝 {product.description[:100] + '...' if len(product.description) > 100 else product.description}")
            description_label.setStyleSheet("color: #666666; font-size: 8pt;")
            description_label.setWordWrap(True)
            info_layout.addWidget(description_label)
        
        info_layout.addStretch()
        
        # Добавляем части в основную карточку
        main_layout.addWidget(photo_frame)
        main_layout.addWidget(info_widget)
        
        # Событие клика для выбора карточки
        card_widget.mousePressEvent = lambda e, card=card_widget: self.select_card(card)
        
        return card_widget

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
        """Активирует/деактивирует кнопки редактирования и удаления"""
        has_selection = self._selected_card is not None
        
        # Включаем кнопки только если есть выделение и пользователь администратор
        if has_selection and self.role_name == "Администратор":
            self.ui.btn_edit.setEnabled(True)
            self.ui.btn_delete.setEnabled(True)
        else:
            self.ui.btn_edit.setEnabled(False)
            self.ui.btn_delete.setEnabled(False)

    def handle_add(self):
        if self._edit_window and self._edit_window.isVisible():
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Окно добавления/редактирования уже открыто")
            return
        try:
            self._edit_window = ProductEditWindow(parent=self)
            self._edit_window.saved.connect(self.on_edit_saved)
            self._edit_window.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось открыть окно редактирования: {str(e)}")
            print(f"Error opening edit window: {e}")  # Для отладки

    def handle_edit(self):
        if not self._selected_card:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите товар для редактирования")
            return
        
        try:
            pid = self._selected_card.property("product_id")
            self.open_edit(pid)
        except (ValueError, AttributeError) as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось получить ID товара: {str(e)}")
            print(f"Error parsing product ID: {e}")

    def open_edit(self, product_id: int):
        if self._edit_window and self._edit_window.isVisible():
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Окно добавления/редактирования уже открыто")
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
        self._selected_card = None
        self.update_buttons_state()

    def handle_delete(self):
        if not self._selected_card:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите товар для удаления")
            return
        
        try:
            pid = self._selected_card.property("product_id")
            
            product_name = "Неизвестный товар"
            for child in self._selected_card.findChildren(QtWidgets.QLabel):
                if child.text() and len(child.text()) < 100:
                    product_name = child.text()
                    break
            
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
            self._selected_card = None
            self.update_buttons_state()
            
        except (ValueError, AttributeError) as e:
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
            QtWidgets.QMessageBox.warning(self, "Предупреждение", f"Окно заказов недоступно: {e}")

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