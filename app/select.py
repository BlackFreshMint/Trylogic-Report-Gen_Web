import os
import sqlite3

# Path to the database
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory where the script is located
db_path = os.path.join(script_dir, 'plantilla_data.db')  # Database path

# Check if the database file exists
if not os.path.exists(db_path):
    print(f"Error: Database file not found at {db_path}")
    print(f"Files in script directory: {os.listdir(script_dir)}")
    exit(1)

# Connect to SQLite database
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# Query the data
try:
    cursor.execute('SELECT * FROM plantilla_data')
    rows = cursor.fetchall()

    if rows:
        print("Data in 'plantilla_data' table:")
        print("---------------------------------------------------------------------")
        for row in rows:
            print(row)
    else:
        print("No data found in 'plantilla_data' table.")
except sqlite3.Error as e:
    print(f"Error querying the database: {e}")
finally:
    # Close the connection
    conn.close()
    print("Database connection closed.")
