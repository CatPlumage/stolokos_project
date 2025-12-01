import os
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import pyqtSignal
from ui.ui_products import Ui_ProductsWindow  # only for reference of widgets not used here
from crud.products import create_product, get_product_by_id, update_product
from crud.references import get_all_categories, get_all_manufacturers, get_all_suppliers

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

class ProductEditWindow(QtWidgets.QWidget):
    saved = pyqtSignal()

    def __init__(self, product_id:int=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить / Редактировать товар")
        self.setMinimumSize(600, 450)
        self.product_id = product_id
        self.old_image = None

        layout = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QFormLayout()
        self.input_name = QtWidgets.QLineEdit()
        self.cmb_category = QtWidgets.QComboBox()
        self.cmb_manufacturer = QtWidgets.QComboBox()
        self.cmb_supplier = QtWidgets.QComboBox()
        self.input_price = QtWidgets.QDoubleSpinBox()
        self.input_price.setMaximum(1e9)
        self.input_price.setDecimals(2)
        self.input_quantity = QtWidgets.QSpinBox()
        self.input_quantity.setMaximum(10**6)
        self.input_discount = QtWidgets.QDoubleSpinBox()
        self.input_discount.setRange(0, 100)
        self.input_discount.setDecimals(2)
        self.input_description = QtWidgets.QTextEdit()
        self.lbl_image = QtWidgets.QLabel()
        self.lbl_image.setFixedSize(300,200)
        self.btn_choose_image = QtWidgets.QPushButton("Выбрать изображение")
        self.btn_remove_image = QtWidgets.QPushButton("Удалить изображение")

        form.addRow("Наименование:", self.input_name)
        form.addRow("Категория:", self.cmb_category)
        form.addRow("Производитель:", self.cmb_manufacturer)
        form.addRow("Поставщик:", self.cmb_supplier)
        form.addRow("Цена:", self.input_price)
        form.addRow("Количество:", self.input_quantity)
        form.addRow("Скидка %:", self.input_discount)
        form.addRow("Описание:", self.input_description)
        form.addRow("Фото (макс 300x200):", self.lbl_image)
        form.addRow("", self.btn_choose_image)
        form.addRow("", self.btn_remove_image)

        layout.addLayout(form)

        btns = QtWidgets.QHBoxLayout()
        self.btn_save = QtWidgets.QPushButton("Сохранить")
        self.btn_cancel = QtWidgets.QPushButton("Отмена")
        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_choose_image.clicked.connect(self.choose_image)
        self.btn_remove_image.clicked.connect(self.remove_image)
        self.btn_save.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(self.close)

        self._fill_refs()

        if self.product_id:
            self._load_product()

    def _fill_refs(self):
        self.cmb_category.clear()
        self.cmb_manufacturer.clear()
        self.cmb_supplier.clear()

        cats = get_all_categories()
        mans = get_all_manufacturers()
        sups = get_all_suppliers()

        self.cmb_category.addItem("", None)
        for c in cats:
            self.cmb_category.addItem(c.name, c.id)

        self.cmb_manufacturer.addItem("", None)
        for m in mans:
            self.cmb_manufacturer.addItem(m.name, m.id)

        self.cmb_supplier.addItem("", None)
        for s in sups:
            self.cmb_supplier.addItem(s.name, s.id)

    def _load_product(self):
        p = get_product_by_id(self.product_id)
        if not p:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Товар не найден")
            self.close()
            return
        self.input_name.setText(p.name)
        # select category by id
        if p.category:
            idx = self.cmb_category.findData(p.category.id)
            if idx != -1:
                self.cmb_category.setCurrentIndex(idx)
        if p.manufacturer:
            idx = self.cmb_manufacturer.findData(p.manufacturer.id)
            if idx != -1:
                self.cmb_manufacturer.setCurrentIndex(idx)
        if p.supplier:
            idx = self.cmb_supplier.findData(p.supplier.id)
            if idx != -1:
                self.cmb_supplier.setCurrentIndex(idx)
        self.input_price.setValue(float(p.price) if p.price else 0.0)
        self.input_quantity.setValue(int(p.quantity or 0))
        self.input_discount.setValue(float(p.discount or 0.0))
        self.input_description.setPlainText(p.description or "")

        if p.image_path:
            full = os.path.join(PROJECT_DIR, "images", p.image_path)
            if os.path.exists(full):
                pix = QtGui.QPixmap(full)
                if not pix.isNull():
                    pix = pix.scaled(self.lbl_image.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                    self.lbl_image.setPixmap(pix)
                    self.old_image = p.image_path

    def choose_image(self):
        fp, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Images (*.png *.jpg *.jpeg)")
        if not fp:
            return
        pix = QtGui.QPixmap(fp)
        if pix.isNull():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Невозможно загрузить изображение")
            return
        # Resize to 300x200 max and save copy to images/
        im = pix.scaled(300, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        # generate unique filename
        base = os.path.basename(fp)
        name = f"{QtCore.QDateTime.currentDateTime().toSecsSinceEpoch()}_{base}"
        dest = os.path.join(IMAGES_DIR, name)
        im.save(dest)
        # display
        self.lbl_image.setPixmap(im)
        self.new_image = name

    def remove_image(self):
        self.lbl_image.clear()
        self.new_image = None
        # mark old_image to be removed on save if desired
        self.removed_image = True

    def save(self):
        name = self.input_name.text().strip()
        if not name:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите наименование")
            return
        price = float(self.input_price.value())
        if price < 0:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Цена не может быть отрицательной")
            return
        qty = int(self.input_quantity.value())
        if qty < 0:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Количество не может быть отрицательным")
            return
        discount = float(self.input_discount.value())
        # prepare fields
        category_id = self.cmb_category.currentData()
        manufacturer_id = self.cmb_manufacturer.currentData()
        supplier_id = self.cmb_supplier.currentData()
        description = self.input_description.toPlainText().strip()

        image_filename = getattr(self, "new_image", None) or getattr(self, "old_image", None)

        if self.product_id:
            # update
            try:
                update_product(self.product_id,
                               name=name,
                               category_id=category_id,
                               manufacturer_id=manufacturer_id,
                               supplier_id=supplier_id,
                               price=price,
                               quantity=qty,
                               discount=discount,
                               description=description,
                               image_path=image_filename)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
                return
            QtWidgets.QMessageBox.information(self, "Готово", "Товар обновлён")
        else:
            try:
                create_product(name=name, category_id=category_id, manufacturer_id=manufacturer_id,
                               supplier_id=supplier_id, price=price, quantity=qty, discount=discount,
                               description=description, image_path=image_filename)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
                return
            QtWidgets.QMessageBox.information(self, "Готово", "Товар добавлен")

        # remove old image file if replaced
        if getattr(self, "old_image", None) and getattr(self, "new_image", None) and self.old_image != self.new_image:
            old_full = os.path.join(IMAGES_DIR, self.old_image)
            try:
                if os.path.exists(old_full):
                    os.remove(old_full)
            except Exception:
                pass

        self.saved.emit()
        self.close()
