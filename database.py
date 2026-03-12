import sqlite3
import os

def init_db():
    """Initialize the database with schema if it doesn't exist"""
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

def get_db():
    init_db()
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn