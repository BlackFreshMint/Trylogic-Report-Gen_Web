import sqlite3
import pandas as pd

# Paths
plantilla_csv_path = 'plantilla_csv.csv'  # Path to the CSV file
db_path = 'plantilla_data.db'  # Database path

# Connect to SQLite (this creates the database if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the table (if not exists)
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

# Commit the table creation
conn.commit()

# Read the CSV file
df = pd.read_csv(plantilla_csv_path, header=None)

# Extract relevant rows (from row 7 to 15)
data_rows = df.iloc[6:15].reset_index(drop=True)

# Process load data (the first row contains the load details)
load_data = data_rows.iloc[0, :8].tolist()  # First 8 columns: Load Size, Ticket, Mix, etc.
load_data = [str(x) if isinstance(x, float) and pd.isna(x) else x for x in load_data]

# Process material data (remaining rows contain material details)
materials_data = []
for _, row in data_rows.iloc[1:].iterrows():
    # Extract relevant columns (Material, Target, Actual, Unit, % Var, Moisture)
    material_data = row.iloc[:7].tolist()  # First 7 columns: Material, Target, Actual, etc.
    material_data = [str(x) if isinstance(x, float) and pd.isna(x) else x for x in material_data]

    # Combine the load data and material data (ensure 15 values)
    # Add placeholders for missing values to ensure 15 values in total
    combined_data = load_data[:8] + material_data[:7]  # 8 from load_data, 7 from material_data
    if len(combined_data) < 15:  # Ensure the total length is 15
        combined_data.append(None)  # Add a placeholder for missing value to make the total 15 columns

    materials_data.append(combined_data)

# Insert the data into the database
for material_entry in materials_data:
    if len(material_entry) == 15:  # Ensure exactly 15 values per entry
        cursor.execute('''
        INSERT INTO plantilla_data (
            Date, Load_Size, Ticket, Mix, Truck, "Order", Project, "Target_W/C",
            "Actual_W/C", Material, Target, Actual, Unit, "% Var", Moisture
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', material_entry)
    else:
        print(f"Error: Invalid number of columns in the row: {material_entry}")

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()

print("Data successfully inserted into the database.")
