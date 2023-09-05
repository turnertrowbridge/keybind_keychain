import database
import sys
from PyQt6.QtWidgets import QApplication
from gui_app import AutoCompleteApp

from trie import Trie

# TODO: Split this into multiple files

# TODO: Load data from database into trie, and use trie to autocomplete search box

DB_NAME = "kb_ky_database.db"


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

    shortcut_2 = database.Shortcut(
        2,
        "Vim",
        "delete word",
        "dw",
        "Deletes word and saves to clipboard",
    )
    db.add_entry(shortcut_2)

    shortcut_3 = database.Shortcut(
        3,
        "Vim",
        "delete character",
        "x",
        "Deletes character and saves to clipboard",
    )
    db.add_entry(shortcut_3)

    shortcut_4 = database.Shortcut(
        4,
        "Chrome",
        "open new tab",
        "ctrl+t",
        "Opens a new tab in Chrome",
    )
    db.add_entry(shortcut_4)

    app = QApplication(sys.argv)
    ex = AutoCompleteApp()
    ex.show()  # Show the main window

    db._delete_db()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
