import sqlite3
import os

def fetch_all_data(db_path):
    if not db_path or not isinstance(db_path, str):
        raise ValueError("Database path is invalid")

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM plantilla_data')
        rows = cursor.fetchall()
        return rows if rows else []
    except sqlite3.Error as e:
        raise Exception(f"Error querying the database: {e}")
    finally:
        conn.close()
