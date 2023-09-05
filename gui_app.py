from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QComboBox, QTableWidget, \
    QHeaderView, QTableWidgetItem
from typing import List

from trie import Trie

import database

DB_NAME = "kb_ky_database.db"

class AutoCompleteApp(QWidget):
    def __init__(self):
        super().__init__()
        # keep the state of which app is selected
        self.selected_app = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # load names into comboBox
        self.comboBox = QComboBox(self)
        app_names = self.load_app_names()
        self.comboBox.addItem("Any Application")
        for app_name in app_names:
            self.comboBox.addItem(app_name)
        layout.addWidget(self.comboBox)

        # adds the custom search box for autocomplete
        self.search_box = AutoCompleteTextBox(self)
        layout.addWidget(self.search_box)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Keybind Keychain🔑')

        # connect to comboBox signal
        self.comboBox.currentTextChanged.connect(self.app_selected)

    def load_app_names(self) -> List[str]:
        applications_list = database.Database(DB_NAME).get_applications()
        app_names = [app.name for app in applications_list]
        return app_names

    def app_selected(self):
        selected_app = self.comboBox.currentText()
        self.selected_app = selected_app if selected_app != "Any Application" else None
        self.search_box.show_suggestions()


class AutoCompleteTextBox(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.text_box = QLineEdit(self)
        self.suggestion_table = QTableWidget(self)
        self.suggestion_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.layout.addWidget(self.text_box)
        self.layout.addWidget(self.suggestion_table)

        # Create and load the Trie with data from the database
        self.master_trie = Trie()
        self.trie_list = []
        self.load_trie_data()

    def load_trie_data(self):
        # load apps
        app_hash_list = []
        applications_list = database.Database(DB_NAME).get_applications()
        for app in applications_list:
            # get all the shortcuts for the app
            app_shortcuts = database.Database(DB_NAME).get_shortcuts_by_app(app.name)

            # store the app's shortcuts in a trie
            app_trie = Trie()
            for shortcut in app_shortcuts:
                app_trie.insert(shortcut.shortcut, shortcut)
            self.trie_list.append((app.name, app_trie))

        # load shortcuts
        shortcuts_list = database.Database(DB_NAME).get_shortcuts()
        for shortcut in shortcuts_list:
            self.master_trie.insert(shortcut.shortcut, shortcut)

        # Connect textChanged signal to show suggestions
        self.text_box.textChanged.connect(self.show_suggestions)

        # show all suggestions by default
        self.show_suggestions()

    def show_suggestions(self):
        prefix = self.text_box.text()

        suggestions = []
        # Load suggestions for a specific app if one is selected, otherwise load suggestions for all apps
        if selected_app := self.parent().selected_app:
            for app in self.trie_list:
                if app[0] == selected_app:
                    suggestions = app[1].search_all(prefix.lower())
        else:
            suggestions = self.master_trie.search_all(prefix.lower())

        # Clear the table
        self.suggestion_table.setRowCount(0)
        self.suggestion_table.setColumnCount(4)
        self.suggestion_table.setHorizontalHeaderLabels(["App", "Shortcut", "Keybinding", "Description"])

        # Populate the table with suggestions
        for shortcut in suggestions:
            row_position = self.suggestion_table.rowCount()
            self.suggestion_table.insertRow(row_position)
            self.suggestion_table.setItem(row_position, 0, QTableWidgetItem(shortcut[1].app))
            self.suggestion_table.setItem(row_position, 1, QTableWidgetItem(shortcut[1].shortcut))
            self.suggestion_table.setItem(row_position, 2, QTableWidgetItem(shortcut[1].keybinding))
            self.suggestion_table.setItem(row_position, 3, QTableWidgetItem(shortcut[1].description))

        # self.suggestion_table.setColumnWidth(3, 300)
        self.suggestion_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.suggestion_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)