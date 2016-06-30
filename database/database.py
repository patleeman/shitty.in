import sqlite3
import os

class Database(object):
    def __init__(self):
        self.database_file = 'db.sqlite3'
        self._check_db_file()

    def __enter__(self):
        self.conn = sqlite3.connect(self.database_file)

    def _check_db_file(self):
        if not os.path.isfile(self.database_file):
            file = open(self.database_file, 'w+')

    def _initialize_tables(self):
        db = Database()
        db.execute('CREATE TABLE IF NOT EXISTS weather (id INT PRIMARY KEY NOT NULL, )')

    def select(self, query):
        if "select" not in query.lower():
            raise ValueError("Query must be a select statement")

        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def execute(self, query):
        self.conn.execute(query)
        self.conn.commit()

    def __exit__(self, type, value, traceback):
        self.conn.close()
