from database.db import get_db_connection
from collections import namedtuple

# Define a Product namedtuple for easier data handling
Product = namedtuple("Product", ["id", "name", "quantity", "price"])


def add_product(name, quantity, price, description=""):
    """Add a new product to the inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, quantity, price, description) VALUES (?, ?, ?, ?)",
        (name, quantity, price, description),
    )
    conn.commit()
    conn.close()
    return True


def get_all_products():
    """Get all products from the inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, quantity, price FROM products")
    products = [
        Product(id=row[0], name=row[1], quantity=row[2], price=row[3])
        for row in cursor.fetchall()
    ]

    conn.close()
    return products


def get_product(product_id):
    """Get a specific product by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, quantity, price FROM products WHERE id = ?", (product_id,)
    )
    product = cursor.fetchone()

    conn.close()

    if product:
        return Product(
            id=product[0], name=product[1], quantity=product[2], price=product[3]
        )
    return None


def update_stock(product_id, new_quantity):
    """Update the stock quantity of a product."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id)
    )
    conn.commit()
    conn.close()
    return True


def delete_product(product_id):
    """Delete a product from the inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return True


def search_products(query):
    """Search for products by name."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, quantity, price FROM products WHERE name LIKE ?",
        (f"%{query}%",),
    )
    products = [
        Product(id=row[0], name=row[1], quantity=row[2], price=row[3])
        for row in cursor.fetchall()
    ]

    conn.close()
    return products
