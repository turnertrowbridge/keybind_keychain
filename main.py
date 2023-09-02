import database
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QLineEdit, QListWidget, \
    QListWidgetItem

from trie import Trie


# def gui():
#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     window.setWindowTitle("Shortcut Manager")
#     window.setGeometry(100, 100, 500, 200)
#     label = QLabel("This is a label", window)
#     label.move(50, 50)
#     window.show()
#     sys.exit(app.exec())


class AutoCompleteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # adds the custom search box for autocomplete
        self.search_box = AutoCompleteTextBox(self)
        layout.addWidget(self.search_box)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('AutoComplete App')


class AutoCompleteTextBox(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.text_box = QLineEdit(self)
        self.suggestion_list = QListWidget(self)
        self.layout.addWidget(self.text_box)
        self.layout.addWidget(self.suggestion_list)

        # Create and load the Trie with sample words
        self.trie = Trie()
        # You can fetch words from your database instead of using sample words
        sample_words = ["apple", "appetizer", "banana", "bat", "ball", "cat", "dog", "doghouse"]
        for word in sample_words:
            self.trie.insert(word)

        # Connect textChanged signal to show suggestions
        self.text_box.textChanged.connect(self.show_suggestions)

    def show_suggestions(self):
        prefix = self.text_box.text()
        suggestions = self.trie.search_all(prefix)

        self.suggestion_list.clear()
        self.suggestion_list.addItems(suggestions)


def main():
    app_db = database.Database("applications.db", database.DatabaseType.Applications)
    app_db.build_db()

    app = QApplication(sys.argv)
    ex = AutoCompleteApp()
    ex.show()  # Show the main window
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
