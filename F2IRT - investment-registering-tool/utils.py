import sqlite3
from datetime import datetime
import os

def create_database():
    dir_path = os.path.join(os.getcwd(), "database")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    connection = sqlite3.connect(os.path.join(dir_path, "operations.db"))
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_type TEXT NOT NULL,
            operation_type TEXT NOT NULL,
            ticker TEXT NOT NULL,
            date TEXT NOT NULL,
            unit_price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            liquidation_fee REAL NOT NULL,
            emoluments_fee REAL NOT NULL,
            taxes REAL NOT NULL DEFAULT 0,
            operational_fee REAL NOT NULL DEFAULT 0,
            other_fees REAL NOT NULL DEFAULT 0,
            irrf REAL NOT NULL DEFAULT 0,
            timestamp TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

def register_operation(asset_type, operation_type, ticker, date, unit_price, quantity, liquidationFee, emolumentsFee, taxes, operationalFee, otherFees, irrf):
    dir_path = os.path.join(os.getcwd(), "database")
    connection = sqlite3.connect(os.path.join(dir_path, "operations.db"))
    cursor = connection.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO operations (asset_type, operation_type, ticker, date, unit_price, quantity, liquidation_fee, emoluments_fee, taxes, operational_fee, other_fees, irrf, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (asset_type, operation_type, ticker, date, unit_price, quantity, liquidationFee, emolumentsFee, taxes, operationalFee, otherFees, irrf, timestamp))
    connection.commit()
    connection.close()

def get_operations():
    dir_path = os.path.join(os.getcwd(), "database")
    connection = sqlite3.connect(os.path.join(dir_path, "operations.db"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM operations")
    results = cursor.fetchall()
    connection.close()
    return results

def get_paginated_operations(page, per_page):
    offset = (page - 1) * per_page
    dir_path = os.path.join(os.getcwd(), "database")
    connection = sqlite3.connect(os.path.join(dir_path, "operations.db"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM operations LIMIT ? OFFSET ?", (per_page, offset))
    results = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM operations")
    total_records = cursor.fetchone()[0]
    connection.close()
    return results, total_records

def delete_record(id):
    dir_path = os.path.join(os.getcwd(), "database")
    connection = sqlite3.connect(os.path.join(dir_path, "operations.db"))
    cursor = connection.cursor()
    cursor.execute("DELETE FROM operations WHERE id = ?", (id,))
    connection.commit()
    connection.close()