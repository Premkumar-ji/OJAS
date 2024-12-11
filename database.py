import sqlite3
import os

def get_database_path():
    """
    Returns the path to the SQLite database file in the same directory as the script.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "contacts.db")


def create_database():
    """
    Creates the SQLite database and initializes the contacts table.
    """
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create contacts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    # Add sample contacts (if not already present)
    sample_contacts = [
        ("me", "+919XXXXXXXX3"),
        ("john", "+912XXXXXX01"),
        ("friend", "+91XXXXXXXXX0")
    ]
    cursor.executemany("INSERT OR IGNORE INTO contacts (name, phone) VALUES (?, ?)", sample_contacts)
    conn.commit()
    conn.close()


def get_phone_number(name):
    """
    Fetches the phone number for a given name from the database.
    """
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT phone FROM contacts WHERE name = ?", (name.lower(),))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None
