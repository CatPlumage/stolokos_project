# product_edit_window.py
import os
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import pyqtSignal
from ui.ui_product_edit import Ui_ProductEditWindow
from crud.products import create_product, get_product_by_id, update_product
from crud.references import get_all_categories, get_all_manufacturers, get_all_suppliers

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

class ProductEditWindow(QtWidgets.QDialog):
    saved = pyqtSignal()

    def __init__(self, product_id=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProductEditWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.product_id = product_id
        self.old_image = None
        self.new_image = None
        self.removed_image = False

        # Подключение сигналов
        self.ui.btn_choose_image.clicked.connect(self.choose_image)
        self.ui.btn_remove_image.clicked.connect(self.remove_image)
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_cancel.clicked.connect(self.reject)

        self._fill_refs()
        if self.product_id:
            self._load_product()

    def _fill_refs(self):
        self.ui.cmb_category.clear()
        self.ui.cmb_manufacturer.clear()
        self.ui.cmb_supplier.clear()
        cats = get_all_categories()
        mans = get_all_manufacturers()
        sups = get_all_suppliers()
        self.ui.cmb_category.addItem("", None)
        for c in cats:
            self.ui.cmb_category.addItem(c.name, c.id)
        self.ui.cmb_manufacturer.addItem("", None)
        for m in mans:
            self.ui.cmb_manufacturer.addItem(m.name, m.id)
        self.ui.cmb_supplier.addItem("", None)
        for s in sups:
            self.ui.cmb_supplier.addItem(s.name, s.id)

    def _load_product(self):
        p = get_product_by_id(self.product_id)
        if not p:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Товар не найден")
            self.reject()
            return
        self.ui.input_name.setText(p.name)
        
        if p.category and hasattr(p.category, 'id'):
            idx = self.ui.cmb_category.findData(p.category.id)
            if idx != -1:
                self.ui.cmb_category.setCurrentIndex(idx)
        
        if p.manufacturer and hasattr(p.manufacturer, 'id'):
            idx = self.ui.cmb_manufacturer.findData(p.manufacturer.id)
            if idx != -1:
                self.ui.cmb_manufacturer.setCurrentIndex(idx)
        
        if p.supplier and hasattr(p.supplier, 'id'):
            idx = self.ui.cmb_supplier.findData(p.supplier.id)
            if idx != -1:
                self.ui.cmb_supplier.setCurrentIndex(idx)
        if not p:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Товар не найден")
            self.reject()
            return
        self.ui.input_name.setText(p.name)
        if p.category:
            idx = self.ui.cmb_category.findData(p.category.id)
            if idx != -1:
                self.ui.cmb_category.setCurrentIndex(idx)
        if p.manufacturer:
            idx = self.ui.cmb_manufacturer.findData(p.manufacturer.id)
            if idx != -1:
                self.ui.cmb_manufacturer.setCurrentIndex(idx)
        if p.supplier:
            idx = self.ui.cmb_supplier.findData(p.supplier.id)
            if idx != -1:
                self.ui.cmb_supplier.setCurrentIndex(idx)
        self.ui.input_price.setValue(float(p.price) if p.price else 0.0)
        self.ui.input_quantity.setValue(int(p.quantity or 0))
        self.ui.input_discount.setValue(float(p.discount or 0.0))
        self.ui.input_description.setPlainText(p.description or "")
        if p.image_path:
            full = os.path.join(PROJECT_DIR, "images", p.image_path)
            if os.path.exists(full):
                pix = QtGui.QPixmap(full)
                if not pix.isNull():
                    pix = pix.scaled(self.ui.lbl_image.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                    self.ui.lbl_image.setPixmap(pix)
                    self.old_image = p.image_path

    def choose_image(self):
        fp, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выбрать изображение", "", "Images (*.png *.jpg *.jpeg)"
        )
        if not fp:
            return
        pix = QtGui.QPixmap(fp)
        if pix.isNull():
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Невозможно загрузить изображение")
            return
        im = pix.scaled(
            300, 200,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        base = os.path.basename(fp)
        name = f"{QtCore.QDateTime.currentDateTime().toSecsSinceEpoch()}_{base}"
        dest = os.path.join(IMAGES_DIR, name)
        im.save(dest)
        self.ui.lbl_image.setPixmap(im)
        self.new_image = name

    def remove_image(self):
        self.ui.lbl_image.clear()
        self.new_image = None
        self.removed_image = True

    def save(self):
        name = self.ui.input_name.text().strip()
        if not name:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Введите наименование")
            return
        price = float(self.ui.input_price.value())
        if price < 0:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Цена не может быть отрицательной")
            return
        qty = int(self.ui.input_quantity.value())
        if qty < 0:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Количество не может быть отрицательным")
            return
        discount = float(self.ui.input_discount.value())

        category_id = self.ui.cmb_category.currentData()
        manufacturer_id = self.ui.cmb_manufacturer.currentData()
        supplier_id = self.ui.cmb_supplier.currentData()
        description = self.ui.input_description.toPlainText().strip()
        image_filename = self.new_image or self.old_image

        try:
            if self.product_id:
                update_product(
                    self.product_id, name=name, category_id=category_id,
                    manufacturer_id=manufacturer_id, supplier_id=supplier_id,
                    price=price, quantity=qty, discount=discount,
                    description=description, image_path=image_filename
                )
                QtWidgets.QMessageBox.information(self, "Готово", "Товар обновлён")
            else:
                create_product(
                    name=name, category_id=category_id, manufacturer_id=manufacturer_id,
                    supplier_id=supplier_id, price=price, quantity=qty, discount=discount,
                    description=description, image_path=image_filename
                )
                QtWidgets.QMessageBox.information(self, "Готово", "Товар добавлен")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
            return

        # Удаление старого изображения, если оно заменено
        if self.old_image and self.new_image and self.old_image != self.new_image:
            old_path = os.path.join(IMAGES_DIR, self.old_image)
            try:
                if os.path.exists(old_path):
                    os.remove(old_path)
            except Exception:
                pass

        self.saved.emit()
        self.accept()