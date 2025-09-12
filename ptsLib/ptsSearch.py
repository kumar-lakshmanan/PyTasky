import sys, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMenu, QHeaderView
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

class SearchWindow(QWidget):
    def __init__(self, searchConfig):
        self.searchConfig = searchConfig
        self.allowed_exts = [ext.lower() for ext in searchConfig["fileTypesToSearch"]]
        self.search_paths = searchConfig["foldersToSearch"]
        
        QWidget.__init__(self)        
        uiFile = r"ptsLib\ptsUi\ptsSubWinSearch.ui"
        loadUi(uiFile, self)        

        self.search_box.textChanged.connect(self.run_search)

        # # # enable custom context menu
        # self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)
        
        

    def run_search(self, query):
        """Search files (filenames + content) restricted to allowed extensions"""
        query = query.strip().lower()
        self.table.setRowCount(0)

        if not query:
            return

        words = query.split()
        results = []

        for ftype, folder in self.search_paths.items():
            for root, dirs, files in os.walk(folder):
                for fname in files:
                    ext = os.path.splitext(fname)[1][1:].lower()  # get extension without "."
                    if ext not in self.allowed_exts:
                        continue

                    full_path = os.path.join(root, fname)
                    try:
                        with open(full_path, "r", encoding="ascii", errors="ignore") as f:
                            content = f.read().lower()
                    except Exception:
                        continue

                    # check if ALL words are in filename or file content
                    if all(w in fname.lower() or w in content for w in words):
                        results.append((fname, ftype, full_path))

        # populate table
        self.table.setRowCount(len(results))
        for row, (fname, ftype, full_path) in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(fname.replace(".py","").replace(".PY","")))
            self.table.setItem(row, 1, QTableWidgetItem(ftype))
            self.table.setItem(row, 2, QTableWidgetItem(full_path))
            self.table.item(row, 0).setData(Qt.UserRole, full_path)

    def open_context_menu(self, pos: QPoint):
        item = self.table.itemAt(pos)
        if item is None:
            return

        row = item.row()
        fname = self.table.item(row, 0).text()
        ftype = self.table.item(row, 1).text()
        full_path = self.table.item(row, 0).data(Qt.UserRole)

        menu = QMenu(self)
        for action_name in ["Edit", "Execute", "Goto Folder"]:
            act = menu.addAction(action_name)
            act.triggered.connect(
                lambda chk, a=action_name: self.handle_action(fname, full_path, ftype, a)
            )

        menu.exec_(self.table.viewport().mapToGlobal(pos))

    def handle_action(self, fname, full_path, ftype, action):
        print(f"{fname} | {full_path} | {ftype} | {action}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # config
    searchConfig = {
        "fileTypesToSearch": ["py", "txt"],
        "foldersToSearch": {
            "Flows": r"G:\pyworkspace\PyTasky\data\ptsFlows",
            "Nodes": r"G:\pyworkspace\PyTasky\data\ptsNodes",
            "Scripts": r"G:\pyworkspace\PyTasky\data\ptsScripts"
        }
    }

    win = SearchWindow(searchConfig)
    win.show()
    sys.exit(app.exec_())
