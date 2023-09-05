from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QTableWidget, \
    QHeaderView, QTableWidgetItem, QPushButton, QHBoxLayout, QDialog, QLabel
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
        self.load_app_names_combobox()
        layout.addWidget(self.comboBox)

        self.button_layout = QHBoxLayout()

        # button to add shortcuts (and apps if needed)
        self.add_button = QPushButton("Add Shortcut")
        self.add_button.clicked.connect(self.add_new)
        self.add_button.setFixedWidth(150)
        self.button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Shortcut")
        self.edit_button.clicked.connect(self.edit_app)
        self.edit_button.setFixedWidth(150)
        self.button_layout.addWidget(self.edit_button)

        # add buttons
        layout.addLayout(self.button_layout)

        # adds the custom search box for autocomplete
        self.search_box = AutoCompleteTextBox(self)
        layout.addWidget(self.search_box)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Keybind Keychain🔑')

        # connect to comboBox signal
        self.comboBox.currentTextChanged.connect(self.app_selected)

        # FIXME: Temporary way to delete database in testing
        self.destroyed.connect(lambda: database.Database(DB_NAME)._delete_db())

    def load_app_names_combobox(self) -> List[str]:
        applications_list = database.Database(DB_NAME).get_applications()
        app_names = [app.name for app in applications_list]
        self.comboBox.addItem("Any Application")
        for app_name in app_names:
            self.comboBox.addItem(app_name)

    def app_selected(self):
        selected_app = self.comboBox.currentText()
        self.selected_app = selected_app if selected_app != "Any Application" else None
        self.search_box.show_suggestions()

    def add_new(self):
        popup = AddShortcutPopup(self)
        popup.setModal(True)
        # position = self.calculate_popup_position()
        # popup.move(position)
        popup.exec()

    def reload_combo_box(self):
        self.comboBox.clear()
        self.load_app_names_combobox()
        self.comboBox.setCurrentText(self.selected_app)

    # def calculate_popup_position(self):
    #     # Calculate the position of the popup relative to the main window
    #     main_window_rect = self.geometry()
    #     popup_x = self.mapToGlobal(main_window_rect.topRight()).x()
    #     popup_y = self.mapToGlobal(main_window_rect.topRight()).y()
    #     return QPoint(popup_x, popup_y)

    def edit_app(self):
        pass


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


class AddShortcutPopup(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Popup Window")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Add labels and text boxes
        self.label1 = QLabel("App:")
        self.text_box1 = QLineEdit(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.text_box1)

        self.label2 = QLabel("Shortcut:")
        self.text_box2 = QLineEdit(self)
        layout.addWidget(self.label2)
        layout.addWidget(self.text_box2)

        self.label3 = QLabel("Keybinding:")
        self.text_box3 = QLineEdit(self)
        layout.addWidget(self.label3)
        layout.addWidget(self.text_box3)

        self.label4 = QLabel("Description:")
        self.text_box4 = QLineEdit(self)
        layout.addWidget(self.label4)
        layout.addWidget(self.text_box4)

        # Add submit and cancel buttons
        self.submit_button = QPushButton("Submit")
        self.cancel_button = QPushButton("Cancel")
        layout.addWidget(self.submit_button)
        layout.addWidget(self.cancel_button)

        self.submit_button.clicked.connect(self.submit)
        self.cancel_button.clicked.connect(self.cancel)

        self.setLayout(layout)

    def submit(self):
        # Retrieve values from text boxes
        app = self.text_box1.text()
        shortcut = self.text_box2.text()
        keybinding = self.text_box3.text()
        description = self.text_box4.text()

        # Add the values to the database
        app_names = self.load_apps()

        if app not in app_names:
            database.Database(DB_NAME).add_entry(database.Application(0, app))

        database.Database(DB_NAME).add_entry(database.Shortcut(0, app, shortcut, keybinding, description))

        # You can process the values here or close the window
        print("Submitted values:")
        print(f"Label 1: {app}")
        print(f"Label 2: {shortcut}")
        print(f"Label 3: {keybinding}")
        print(f"Label 4: {description}")

        self.parent().reload_combo_box()  # Update the combo box
        self.parent().search_box.load_trie_data()  # Update the suggestions
        self.accept()  # Close the dialog

    def load_apps(self):
        applications_list = database.Database(DB_NAME).get_applications()
        return [app.name for app in applications_list]

    def cancel(self):
        self.reject()  # Close the dialog without processing
