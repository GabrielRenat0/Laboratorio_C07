import mysql.connector

from config import MYSQL_CONFIG


class DatabaseManager:
    """Holds the MySQL connection and the generic query helpers used by DAOs."""

    def __init__(self, **config):
        self.conn = mysql.connector.connect(**(config or MYSQL_CONFIG))
        self.cursor = self.conn.cursor()
        print(f"Connected to MySQL: {self.conn.database}")

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("Connection closed")

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()
        return self.cursor.lastrowid, self.cursor.rowcount

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()
