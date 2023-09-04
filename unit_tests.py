import unittest
from typing import List

from database import Database, DatabaseType, Application, Shortcut
from trie import Trie

test_calls = 1


def _print_results(entries: List[Application or Shortcut]) -> None:
    _test_call()
    for entry in entries:
        if isinstance(entry, Application):
            print(f"Application - ID: {entry.id}, Name: {entry.name}")
        elif isinstance(entry, Shortcut):
            print(
                f"Shortcut - ID: {entry.id}, App: {entry.app}, Shortcut: {entry.shortcut}, Keybinding: {entry.keybinding}, Description: {entry.description}")
        else:
            print(entry)


def _test_call() -> None:
    global test_calls
    print("")
    print(f"------------ TEST #{test_calls}  ------------")
    test_calls += 1


class TestDatabase(unittest.TestCase):
    def test_app_entry(self) -> None:
        # delete the database if it exists
        test_db = Database("test.db")
        test_db._delete_db()

        # create database
        test_db = Database("test.db")
        test_db.create_applications_table()

        app_1 = Application(1, "Vim")
        test_db.add_entry(app_1)

        app_2 = Application(2, "Firefox")
        test_db.add_entry(app_2)

        app_3 = Application(3, "Chrome")
        test_db.add_entry(app_3)

        tables = test_db.get_tables()
        _print_results(tables)

        # get all entries
        test_results = test_db.get_applications()
        _print_results(test_results)
        self.assertEqual(len(test_results), 3)

        # add shortcuts table
        test_db.create_shortcuts_table()
        shortcut_1 = Shortcut(
            1,
            "Vim",
            "delete line",
            "dd",
            "Deletes line and saves to clipboard"
        )
        test_db.add_entry(shortcut_1)

        test_results = test_db.get_shortcuts()
        _print_results(test_results)
        self.assertEqual(len(test_results), 1)
        self.assertEqual(test_results[0].shortcut, "delete line")

        _print_results(test_db.get_shortcuts_by_app("Vim"))
        self.assertEqual(test_db.get_shortcuts_by_app("Vim")[0].app, "Vim")

        test_db.delete_applications_table()
        test_db.delete_shortcuts_table()
        test_db.close()
        test_db._delete_db()

    # trie testing
    def test_trie(self):
        trie = Trie()
        words = ["apple", "app", "application", "applesauce", "apples", "applet",
                 "appetizer", "appetite", "appetizing"
            , "amazing", "baseball"]
        for word in words:
            trie.insert(word, None)

        _test_call()
        print("apple in trie:", trie.search("apple"))
        self.assertTrue(trie.search("apple"))

        _test_call()
        print("applesauceee in trie:", trie.search("applesauceee"))
        self.assertFalse(trie.search("applesauceee"))

        _test_call()
        print(trie.search_all("app"))
        # self.assertEqual(trie.search_all("app"), ["app", "apple", "apples", "applesauce", "applet",
        #                                           "application", "appetizer", "appetizing", "appetite"])

        _test_call()
        print("Search for am yields:", trie.search_all("am"))
        self.assertEqual(trie.search_all("am"), ["amazing"])

        _test_call()
        print("Search for a yields:", trie.search_all("a"))
        self.assertEqual(trie.search_all("a"), ['app', 'apple', 'apples', 'applesauce', 'applet', 'application',
                                                'appetizer', 'appetizing', 'appetite', 'amazing'])

        _test_call()
        print("Search for a yields:", trie.search_all("base"))
        self.assertEqual(trie.search_all("base"), ["baseball"])


if __name__ == '__main__':
    unittest.main()
