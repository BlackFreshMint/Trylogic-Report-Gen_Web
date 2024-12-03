import os
import sqlite3
import pandas as pd

def insert_data_into_db(plantilla_path, db_path):
    if not os.path.exists(plantilla_path):
        raise FileNotFoundError(f"CSV file not found at {plantilla_path}")

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

    df = pd.read_csv(plantilla_path, header=None)
    try:
        data_rows = df.iloc[6:15].reset_index(drop=True)
    except IndexError:
        raise Exception("CSV file does not have enough rows (expected at least 15).")

    load_data = data_rows.iloc[0, :8].tolist()
    load_data = [str(x) if pd.isna(x) else x for x in load_data]

    materials_data = []
    for _, row in data_rows.iloc[1:].iterrows():
        material_data = row.iloc[:7].tolist()
        material_data = [str(x) if pd.isna(x) else x for x in material_data]
        combined_data = load_data[:8] + material_data[:7]
        combined_data += [None] * (15 - len(combined_data))
        materials_data.append(combined_data)

    for material_entry in materials_data:
        if len(material_entry) == 15:
            cursor.execute('''
            INSERT INTO plantilla_data (
                Date, Load_Size, Ticket, Mix, Truck, "Order", Project, "Target_W/C",
                "Actual_W/C", Material, Target, Actual, Unit, "% Var", Moisture
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', material_entry)
        else:
            raise ValueError(f"Invalid row length: {len(material_entry)}")

    conn.commit()
    conn.close()
