import sqlite3

conn = sqlite3.connect('plantilla_data.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM plantilla_data')

rows = cursor.fetchall()

if rows:
    print("Data in 'plantilla_data' table:")
    print("---------------------------------------------------------------------")
    for row in rows:
        print(row)
else:
    print("No data found in 'plantilla_data' table.")

conn.close()
