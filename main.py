import database
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QComboBox
from typing import List


from trie import Trie

# TODO: Split this into multiple files

# TODO: Load data from database into trie, and use trie to autocomplete search box

DB_NAME = "kb_ky_database.db"

class AutoCompleteApp(QWidget):
    def __init__(self):
        super().__init__()
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

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Keybind Keychain🔑')

    def load_app_names(self) -> List[str]:
        applications_list = database.Database(DB_NAME).get_applications()
        app_names = [app.name for app in applications_list]
        return app_names


class AutoCompleteTextBox(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.text_box = QLineEdit(self)
        self.suggestion_list = QListWidget(self)
        self.layout.addWidget(self.text_box)
        self.layout.addWidget(self.suggestion_list)

        # Create and load the Trie with data from the database
        self.trie = Trie()
        self.load_trie_data()

    def load_trie_data(self):
        # # load apps
        # applications_list = database.Database(DB_NAME).get_applications()
        # for app in applications_list:
        #     self.trie.insert(app.name)
        # load shortcuts
        shortcuts_list = database.Database(DB_NAME).get_shortcuts()
        for shortcut in shortcuts_list:
            self.trie.insert(shortcut.shortcut)

        print(self.trie.search_all(""))

        # Connect textChanged signal to show suggestions
        self.text_box.textChanged.connect(self.show_suggestions)

        # show all suggestions by default
        self.show_suggestions()

    def show_suggestions(self):
        prefix = self.text_box.text()
        suggestions = self.trie.search_all(prefix)

        self.suggestion_list.clear()
        self.suggestion_list.addItems(suggestions)


def main():
    db = database.Database(DB_NAME)
    db.create_applications_table()
    db.create_shortcuts_table()

    app_1 = database.Application(1, "Vim")
    db.add_entry(app_1)
    app_2 = database.Application(2, "Firefox")
    db.add_entry(app_2)
    app_3 = database.Application(3, "Chrome")
    db.add_entry(app_3)

    shortcut_1 = database.Shortcut(
        1,
        "Vim",
        "delete line",
        "dd",
        "Deletes line and saves to clipboard",
    )
    db.add_entry(shortcut_1)



    app = QApplication(sys.argv)
    ex = AutoCompleteApp()
    ex.show()  # Show the main window


    db._delete_db()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
