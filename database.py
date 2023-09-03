import os
import sqlite3
from typing import List


class DatabaseType:
    Applications = 1
    Shortcuts = 2


class Application:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Shortcut:
    def __init__(self, id, app, shortcut, keybinding, description):
        self.id = id
        self.app = app
        self.shortcut = shortcut
        self.keybinding = keybinding
        self.description = description


class Database:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.conn = sqlite3.connect(file_name)
        # self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()

    # create an applications table
    def create_applications_table(self) -> None:
        self.conn.execute("""
               CREATE TABLE IF NOT EXISTS applications (
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL
               )""")
        self.conn.commit()

    # create a shortcuts table
    def create_shortcuts_table(self) -> None:
        self.conn.execute("""
               CREATE TABLE IF NOT EXISTS shortcuts (
               id INTEGER PRIMARY KEY,
               app TEXT NOT NULL,
               shortcut TEXT NOT NULL,
               keybinding TEXT NOT NULL,
               description TEXT NOT NULL
               )""")
        self.conn.commit()

    # add an entry
    def add_entry(self, entry: Application or Shortcut) -> None:
        if isinstance(entry, Application):
            self.conn.execute("INSERT INTO applications (name) VALUES (?)", (entry.name,))
            self.conn.commit()
        elif isinstance(entry, Shortcut):
            self.conn.execute("INSERT INTO shortcuts (app, shortcut, keybinding, description) VALUES (?, ?, ?, ?)",
                              (entry.app, entry.shortcut, entry.keybinding, entry.description))
            self.conn.commit()

    # query the database for applications
    def get_applications(self, max_entries: int = 1000) -> List[Application]:
        query = "SELECT id, name FROM applications"
        query += f" LIMIT {max_entries}"
        cursor = self.conn.execute(query)
        entries = [Application(row[0], row[1]) for row in cursor.fetchall()]
        return entries

    # query the database for shortcuts
    def get_shortcuts(self, max_entries: int = 1000) -> List[Shortcut]:
        query = "SELECT id, app, shortcut, keybinding, description FROM shortcuts"
        query += f" LIMIT {max_entries}"
        cursor = self.conn.execute(query)
        entries = [Shortcut(row[0], row[1], row[2], row[3], row[4]) for row in cursor.fetchall()]
        return entries

    # get all tables
    def get_tables(self) -> List[str]:
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        return tables

    # delete the database, WARNING: this is permanent
    def _delete_db(self) -> None:
        try:
            os.remove(self.file_name)
            print(f"{self.file_name} has been deleted.")
        except FileNotFoundError:
            print(f"{self.file_name} not found.")
        except Exception as e:
            print(f"An error occurred while deleting {self.file_name}: {e}")

    # delete applications table
    def delete_applications_table(self) -> None:
        sql = "DROP TABLE IF EXISTS applications"
        self.conn.execute(sql)
        self.conn.commit()

    # delete shortcuts table
    def delete_shortcuts_table(self) -> None:
        sql = "DROP TABLE IF EXISTS shortcuts"
        self.conn.execute(sql)
        self.conn.commit()

    # close connection
    def close(self) -> None:
        self.conn.close()
