import sqlite3
import os

def clean_database(db_path):
    """Clears all data from the 'plantilla_data' table."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM plantilla_data")
        conn.commit()
        print("Database cleaned successfully.")
    except sqlite3.Error as e:
        raise Exception(f"Error cleaning the database: {e}")
    finally:
        conn.close()
