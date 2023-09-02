import unittest
from typing import List

from database import Database, DatabaseType, Application, Shortcut  # Import your module and classes here
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


def _test_call() -> None:
    global test_calls
    print("")
    print(f"------------ TEST #{test_calls}  ------------")
    test_calls += 1


class TestDatabase(unittest.TestCase):
    def test_app_entry(self) -> None:
        test_application_db = Database("applications_test.db", DatabaseType.Applications)
        test_application_db.build_db()

        app_1 = Application(1, "Vim")
        test_application_db.add_entry(app_1)

        app_2 = Application(2, "Firefox")
        test_application_db.add_entry(app_2)

        app_3 = Application(3, "Chrome")
        test_application_db.add_entry(app_3)

        # get all entries
        test_results = test_application_db.get_entries()
        _print_results(test_results)
        self.assertEqual(len(test_results), 3)

        # get only 2 entries
        limited_results = test_application_db.get_entries(1)
        _print_results(limited_results)
        self.assertEqual(len(limited_results), 1)

        test_application_db.cleanup_table()
        test_application_db.close()

    def test_shortcut_entry(self):
        test_shortcut_db = Database("shortcuts_test.db", DatabaseType.Shortcuts)
        test_shortcut_db.build_db()

        app_1 = Shortcut(
            1,
            "Vim",
            "delete line",
            "dd",
            "Deletes line and saves to clipboard"
        )
        test_shortcut_db.add_entry(app_1)

        test_results = test_shortcut_db.get_entries()
        _print_results(test_results)
        self.assertEqual(len(test_results), 1)
        self.assertEqual(test_results[0].shortcut, "delete line")

        test_shortcut_db.cleanup_table()
        test_shortcut_db.close()

    def test_trie(self):
        trie = Trie()
        words = ["apple", "app", "application", "applesauce", "apples", "applet",
                 "appetizer", "appetite", "appetizing"
                 , "amazing", "baseball"]
        for word in words:
            trie.insert(word)

        _test_call()
        print("apple in trie:", trie.search("apple"))
        self.assertTrue(trie.search("apple"))

        _test_call()
        print("applesauceee in trie:", trie.search("applesauce"))
        self.assertFalse(trie.search("applesauceee"))

        _test_call()
        print(trie.search_all("app"))
        self.assertEqual(trie.search_all("app"), ["app", "apple", "apples", "applesauce", "applet",
                                                  "application", "appetizer", "appetizing", "appetite"])

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
