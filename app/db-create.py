import sqlite3

db_path = 'app/plantilla_data.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS plantilla_data (
    Date TEXT,
    Load_Size REAL,
    Ticket INTEGER,
    Mix TEXT,
    Truck TEXT,
    "Order" INTEGER,
    Project INTEGER,
    "Target_W/C" REAL,
    "Actual_W/C" REAL,
    Material TEXT,
    Target REAL,
    Actual REAL,
    Unit TEXT,
    "% Var" REAL,
    Moisture TEXT
)
''')

conn.commit()
conn.close()

print("Base de datos y tabla 'plantilla_data' creadas correctamente.")
