import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
database_path = os.path.join(BASE_DIR, "data", "app.db")

conn = sqlite3.connect(database_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
conn.close()