import sqlite3

def get_connection():
    # Returns a connection object to the SQLite database
    return sqlite3.connect("inventory.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table (already implemented)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """
    )

    # Create products table (already implemented)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER,
            price REAL
        )
        """
    )

    # Create sales table (for tracking sales)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            date TEXT
        )
        """
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()
