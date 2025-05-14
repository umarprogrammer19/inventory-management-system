import hashlib
from database.db import get_db_connection


def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    """Register a new user."""
    if not username or not password:
        return False

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False

    # Hash the password and store the user
    hashed_password = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password),
    )
    conn.commit()
    conn.close()
    return True


def login_user(username, password):
    """Authenticate a user."""
    if not username or not password:
        return False

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the user
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False

    # Check password
    hashed_password = hash_password(password)
    return hashed_password == user[2]  # Index 2 is the password column
