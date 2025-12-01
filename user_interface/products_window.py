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
    def __init__(self, user=None, parent_main=None):
        super().__init__()
        self.ui = Ui_ProductsWindow()
        self.ui.setupUi(self)
        self.user = user
        self.parent_main = parent_main  # ← ссылка на MainWindow
        # current filtered list
        self._products_cache = []
        self._edit_window = None  # to prevent opening multiple edit windows

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

        # Лейбл пользователя
        if user:
            self.ui.label_user.setText(f"{user.full_name} ({role_name})")
        else:
            self.ui.label_user.setText("Гость")

        # Set user label (дублирующая строка — оставлена как в оригинале)
        if user:
            self.ui.label_user.setText(f"{user.full_name} ({user.role.name})")
        else:
            self.ui.label_user.setText("Гость")

        # Connect signals
        self.ui.btn_back.clicked.connect(self.go_back)
        self.ui.search_input.textChanged.connect(self.apply_filters)
        self.ui.supplier_filter.currentTextChanged.connect(self.apply_filters)
        self.ui.sort_box.currentTextChanged.connect(self.apply_filters)
        self.ui.btn_add.clicked.connect(self.handle_add)
        self.ui.btn_edit.clicked.connect(self.handle_edit)
        self.ui.btn_delete.clicked.connect(self.handle_delete)
        self.ui.table.cellDoubleClicked.connect(self.on_table_double_click)

        # Fill supplier combo
        self._fill_suppliers()

        # Load
        self.load_products()

    def _fill_suppliers(self):
        self.ui.supplier_filter.clear()
        self.ui.supplier_filter.addItem("Все поставщики")
        suppliers = get_all_suppliers()
        for s in suppliers:
            self.ui.supplier_filter.addItem(s.name)

    def load_products(self):
        products = get_all_products()
        print("Products loaded:", products) # ← DEBUG
        self._products_cache = products  # ← ВАЖНО!
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
            # ID, Name, Category, Description, Manufacturer, Supplier
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(p.name))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(p.category.name if p.category else ""))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(p.description or ""))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(p.manufacturer.name if p.manufacturer else ""))
            table.setItem(row, 5, QtWidgets.QTableWidgetItem(p.supplier.name if p.supplier else ""))

            # === PRICE DISPLAY WITH DISCOUNT ===
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
                final_label.setStyleSheet("color: black;")  # Явно задаём чёрный цвет
                final_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

                # Компоновка
                layout = QtWidgets.QHBoxLayout()
                layout.setContentsMargins(2, 0, 2, 0)
                layout.addWidget(original_label)
                layout.addWidget(final_label)
                layout.addStretch()

                container = QtWidgets.QWidget()
                container.setLayout(layout)

                # Убираем фон у контейнера — фон строки будет задан через QTableWidgetItem
                container.setAutoFillBackground(False)  # ← ВАЖНО!

                table.setCellWidget(row, 6, container)
            else:
                # Нет скидки — просто обычная цена
                price_label = QtWidgets.QLabel(f"{base_price:.2f}")
                price_label.setFont(QtGui.QFont("Times New Roman", 8))
                price_label.setStyleSheet("color: black;")  # Явно чёрный цвет
                price_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
                price_label.setAutoFillBackground(False)  # Без фона

                table.setCellWidget(row, 6, price_label)

            # Discount column (остаётся текстовым)
            table.setItem(row, 7, QtWidgets.QTableWidgetItem(f"{discount:.2f}%" if p.discount else "0.00%"))
            table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(p.quantity or 0)))

            # Photo — оставляем как есть, без фона
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

            # Применяем фон ко всем ячейкам строки (кроме тех, где установлен CellWidget — они не поддерживают фон напрямую)
            # Поэтому устанавливаем фон через QTableWidgetItem
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    if bg_color:
                        item.setBackground(bg_color)
                    else:
                        item.setBackground(QtGui.QColor("white"))  # или default

        table.resizeRowsToContents()

    def on_table_double_click(self, row, col):
        # For admin: open edit window on double click on a row; also allowed in spec for "редактировать - при нажатии на конкретный элемент"
        if self.role_name in ("administrator", "admin"):
            item = self.ui.table.item(row, 0)
            if not item:
                return
            product_id = int(item.text())
            self.open_edit(product_id)

    def handle_add(self):
        if self._edit_window and self._edit_window.isVisible():
            QtWidgets.QMessageBox.warning(self, "Внимание", "Окно добавления/редактирования уже открыто")
            return
        self._edit_window = ProductEditWindow(parent=self)
        self._edit_window.saved.connect(self.on_edit_saved)
        self._edit_window.show()

    def handle_edit(self):
        sel = self.ui.table.selectedItems()
        if not sel:
            QtWidgets.QMessageBox.information(self, "Информация", "Выберите товар для редактирования")
            return
        # first column of selected row is ID
        row = sel[0].row()
        item = self.ui.table.item(row, 0)
        if not item:
            return
        pid = int(item.text())
        self.open_edit(pid)

    def open_edit(self, product_id:int):
        if self._edit_window and self._edit_window.isVisible():
            QtWidgets.QMessageBox.warning(self, "Внимание", "Окно добавления/редактирования уже открыто")
            return
        self._edit_window = ProductEditWindow(product_id=product_id, parent=self)
        self._edit_window.saved.connect(self.on_edit_saved)
        self._edit_window.show()

    def on_edit_saved(self):
        # refresh products
        self.load_products()

    def handle_delete(self):
        sel = self.ui.table.selectedItems()
        if not sel:
            QtWidgets.QMessageBox.information(self, "Информация", "Выберите товар для удаления")
            return
        row = sel[0].row()
        item = self.ui.table.item(row, 0)
        if not item:
            return
        pid = int(item.text())

        # confirm
        ok = QtWidgets.QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить товар?")
        if ok != QtWidgets.QMessageBox.StandardButton.Yes:
            return
        try:
            delete_product(pid)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
            return
        QtWidgets.QMessageBox.information(self, "Успех", "Товар удалён")
        self.load_products()

    def go_back(self):
        self.close()
        if self.parent_main:
            self.parent_main.show()
        else:
            # fallback — открываем MainWindow заново
            from user_interface.main_window import MainWindow
            self.main_win = MainWindow(user=self.user)
            self.main_win.show()