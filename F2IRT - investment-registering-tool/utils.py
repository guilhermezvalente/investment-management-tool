import sqlite3
from datetime import datetime
import os

def create_database():
    if not os.path.exists("/F2IRT - investment-registering-tool/database"):
        os.makedirs("/F2IRT - investment-registering-tool/database")

    connection = sqlite3.connect("/F2IRT - investment-registering-tool/database/operations.db")
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


# Register a new operation
def register_operation(asset_type, operation_type, ticker, date, unit_price, quantity, liquidationFee, emolumentsFee, taxes, operationalFee, otherFees, irrf):
    connection = sqlite3.connect("/F2IRT - investment-registering-tool/database/operations.db")
    cursor = connection.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO operations (asset_type, operation_type, ticker, date, unit_price, quantity, liquidation_fee, emoluments_fee, taxes, operational_fee, other_fees, irrf, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (asset_type, operation_type, ticker, date, unit_price, quantity, liquidationFee, emolumentsFee, taxes, operationalFee, otherFees, irrf, timestamp))
    connection.commit()
    connection.close()

# Get all operations
def get_operations():
    connection = sqlite3.connect("/F2IRT - investment-registering-tool/database/operations.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM operations")
    results = cursor.fetchall()
    connection.close()
    return results

# Get paginated operations
def get_paginated_operations(page, per_page):
    offset = (page - 1) * per_page
    connection = sqlite3.connect("/F2IRT - investment-registering-tool/database/operations.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM operations LIMIT ? OFFSET ?", (per_page, offset))
    results = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM operations")
    total_records = cursor.fetchone()[0]
    connection.close()
    return results, total_records
