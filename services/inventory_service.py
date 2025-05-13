from database.db import get_connection
from models.product import Product


def add_product(name, quantity, price):
    # Adds a new product to the products table
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
        (name, quantity, price),
    )
    conn.commit()
    conn.close()


def get_all_products():
    # Fetches all products from the products table
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [Product(*row) for row in rows]  # Create Product objects from rows


def update_stock(product_id, new_quantity):
    # Updates the stock (quantity) of a product
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id)
    )
    conn.commit()
    conn.close()


def delete_product(product_id):
    # Deletes a product from the products table
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
