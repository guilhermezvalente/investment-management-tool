import sqlite3
from datetime import datetime
import os

def create_database():
    if not os.path.exists("database"):
        os.makedirs("database")

    connection = sqlite3.connect("database/operations.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            date TEXT NOT NULL,
            unit_price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            fees REAL NOT NULL,
            taxes REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


# Register a new operation
def register_operation(ticker, date, unit_price, quantity, fees, taxes):
    connection = sqlite3.connect("database/operations.db")
    cursor = connection.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO operations (ticker, date, unit_price, quantity, fees, taxes, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (ticker, date, unit_price, quantity, fees, taxes, timestamp))
    connection.commit()
    connection.close()

# Get all operations
def get_operations():
    connection = sqlite3.connect("database/operations.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM operations")
    results = cursor.fetchall()
    connection.close()
    return results