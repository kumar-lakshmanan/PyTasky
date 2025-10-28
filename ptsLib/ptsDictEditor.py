'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:
'''

__created__ = "2025-10-25"
__updated__ = "2025-10-25"
__author__  = "kayma"

from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTreeWidget, QTreeWidgetItem, QPlainTextEdit, QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import Qt
import json
import sys


class JsonTextEditor(QDialog):
    """Popup editor for complex dict/list values"""
    def __init__(self, value):
        super().__init__()
        self.setWindowTitle("Edit JSON Value")
        layout = QVBoxLayout(self)
        self.text = QPlainTextEdit()
        self.text.setPlainText(json.dumps(value, indent=2))
        layout.addWidget(self.text)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(btns)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

    def get_value(self):
        try:
            return json.loads(self.text.toPlainText())
        except Exception as e:
            QMessageBox.warning(self, "Invalid JSON", str(e))
            return None


class DictEditor(QDialog):
    def __init__(self, data, mode="edit"):
        super().__init__()
        self.setWindowTitle("Dict Editor" if mode == "edit" else "JSON Browser / Selector")
        self.resize(750, 500)
        self.data = data
        self.mode = mode

        layout = QVBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Key / Index", "Value"])
        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionMode(QTreeWidget.ExtendedSelection if mode == "select" else QTreeWidget.SingleSelection)
        self.tree.setStyleSheet("""
            QTreeWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)
        layout.addWidget(self.tree)

        # Editing behavior
        if mode == "edit":
            self.tree.setEditTriggers(QTreeWidget.DoubleClicked | QTreeWidget.SelectedClicked)
        else:
            self.tree.setEditTriggers(QTreeWidget.NoEditTriggers)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.remove_btn = QPushButton("Remove")
        self.ok_btn = QPushButton("OK")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        layout.addLayout(btn_layout)

        if mode == "select":
            self.add_btn.setVisible(False)
            self.remove_btn.setVisible(False)

        self.add_btn.clicked.connect(self.add_item)
        self.remove_btn.clicked.connect(self.remove_item)
        self.ok_btn.clicked.connect(self.accept)

        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.load_data(self.data, self.tree.invisibleRootItem(), "$")

    # ---------- Load Data Recursively ----------
    def make_item(self, key, value="", path="$"):
        item = QTreeWidgetItem([str(key), str(value)])
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setData(0, Qt.UserRole, path)
        return item

    def load_data(self, value, parent, path):
        if isinstance(value, dict):
            for k, v in value.items():
                child_path = f"{path}.{k}"
                item = self.make_item(k, "" if isinstance(v, (dict, list)) else v, child_path)
                parent.addChild(item)
                if isinstance(v, (dict, list)):
                    self.load_data(v, item, child_path)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                child_path = f"{path}[{i}]"
                item = self.make_item(f"[{i}]", "" if isinstance(v, (dict, list)) else v, child_path)
                parent.addChild(item)
                if isinstance(v, (dict, list)):
                    self.load_data(v, item, child_path)

    # ---------- Editing ----------
    def on_item_double_clicked(self, item, column):
        if self.mode != "edit":
            return
        if column == 1 and item.childCount() > 0:
            # complex structure: open JSON editor
            current_value = self.build_data(item)
            editor = JsonTextEditor(current_value)
            if editor.exec_() == QDialog.Accepted:
                new_val = editor.get_value()
                if new_val is not None:
                    item.takeChildren()
                    self.load_data(new_val, item, item.data(0, Qt.UserRole))
                    item.setExpanded(True)

    def add_item(self):
        selected = self.tree.currentItem()
        new_item = self.make_item("newKey", "newValue")
        if selected:
            if selected.childCount() == 0 and selected.text(1):
                selected.setText(1, "")
                selected.addChild(new_item)
            else:
                selected.addChild(new_item)
            selected.setExpanded(True)
        else:
            self.tree.invisibleRootItem().addChild(new_item)

    def remove_item(self):
        selected = self.tree.currentItem()
        if not selected:
            return
        parent = selected.parent()
        if parent:
            parent.removeChild(selected)
        else:
            idx = self.tree.indexOfTopLevelItem(selected)
            self.tree.takeTopLevelItem(idx)

    # ---------- Rebuild Dict ----------
    def build_data(self, parent):
        result = {}
        is_list = all(parent.child(i).text(0).startswith("[") for i in range(parent.childCount()))

        if is_list:
            temp = []
            for i in range(parent.childCount()):
                child = parent.child(i)
                temp.append(self.build_data(child) if child.childCount() else self.parse_value(child.text(1)))
            return temp
        else:
            for i in range(parent.childCount()):
                child = parent.child(i)
                key = child.text(0)
                val = self.build_data(child) if child.childCount() else self.parse_value(child.text(1))
                result[key] = val
            return result

    def parse_value(self, value):
        if value in ("True", "False", "None"):
            return eval(value)
        try:
            if "." in value:
                return float(value)
            else:
                return int(value)
        except Exception:
            return value

    def get_data(self):
        return self.build_data(self.tree.invisibleRootItem())

    def get_selected_paths(self):
        """Return list of JSONPaths for selected nodes (selection mode)"""
        paths = []
        for item in self.tree.selectedItems():
            path = item.data(0, Qt.UserRole)
            if path:
                paths.append(path)
        return paths


def showDictUIEditor(input_dict, mode="edit"):
    """
    mode = 'edit'  -> editable dict editor, returns updated dict
    mode = 'select' -> readonly browser, returns list of JSONPath strings
    """
    app = QApplication.instance()
    own_app = False
    if not app:
        app = QApplication(sys.argv)
        own_app = True

    editor = DictEditor(input_dict, mode)
    editor.exec_()

    if mode == "edit":
        result = editor.get_data()
    else:
        result = editor.get_selected_paths()

    if own_app:
        app.quit()
    return result


# ---------- Test ----------
if __name__ == "__main__":
    d = {
        "product_id": "ABC12345",
        "product_name": "Wirelh",
        "mylist": [{"itm1": "dd"}, {"itm2": "dff"}],
        "mylist2": [{"itm1": ["dd", "cxc"]}, {"itm2": "dff"}],
        "features": ["Noise Cancellation", "Bluetooth 5.0", "Long Battery Life", "Comfortable Fit"],
        "price": 99.99,
        "available_colors": ["Black", "Silver", "Blue"],
        "ratings": {"average": 4.5, "count": 1250},
    }

    #mode = "edit"  # for full edit
    mode = "select"  # try readonly + path selection
    result = showDictUIEditor(d, mode)
    print("\nResult:", result)

