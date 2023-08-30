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
    def __init__(self, file_name: str, db_type: int) -> None:
        self.conn = sqlite3.connect(file_name)
        self.db_type = db_type
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()

    # build the database
    def build_db(self) -> None:
        # create an application database
        if self.db_type == DatabaseType.Applications:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
                )""")
            self.conn.commit()
        # create a shortcut type database
        elif self.db_type == DatabaseType.Shortcuts:
            self.conn.execute("""
                            CREATE TABLE IF NOT EXISTS shortcuts (
                            id INTEGER PRIMARY KEY,
                            app TEXT NOT NULL,
                            shortcut TEXT NOT NULL,
                            keybinding TEXT NOT NULL,
                            description TEXT NOT NULL
                            )""")
            self.conn.commit()

    # add entry to database
    def add_entry(self, entry: Application or Shortcut) -> None:
        if self.db_type == DatabaseType.Applications:
            self.conn.execute("INSERT INTO applications (name) VALUES (?)", (entry.name,))
            self.conn.commit()
        elif self.db_type == DatabaseType.Shortcuts:
            self.conn.execute("INSERT INTO shortcuts (app, shortcut, keybinding, description) VALUES (?, ?, ?, ?)",
                              (entry.app, entry.shortcut, entry.keybinding, entry.description))
            self.conn.commit()

    # query the database for all entries
    def get_entries(self, max_entries: int = None) -> List[Application or Shortcut]:
        if self.db_type == DatabaseType.Applications:
            query = "SELECT id, name FROM applications"
            if max_entries is not None:
                query += f" LIMIT {max_entries}"
            cursor = self.conn.execute(query)
            entries = [Application(row[0], row[1]) for row in cursor.fetchall()]
            return entries
        elif self.db_type == DatabaseType.Shortcuts:
            query = "SELECT id, app, shortcut, keybinding, description FROM shortcuts"
            if max_entries is not None:
                query += f" LIMIT {max_entries}"
            cursor = self.conn.execute(query)
            entries = [Shortcut(row[0], row[1], row[2], row[3], row[4]) for row in cursor.fetchall()]
            return entries

    # clean up table
    def cleanup_table(self) -> None:
        table_name = "applications" if self.db_type == DatabaseType.Applications else "shortcuts"
        sql = f"DROP TABLE IF EXISTS {table_name}"
        self.conn.execute(sql)
        self.conn.commit()

    # close connection
    def close(self) -> None:
        self.conn.close()
