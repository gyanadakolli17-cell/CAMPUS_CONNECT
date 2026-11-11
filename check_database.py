
import sqlite3
from pathlib import Path

# Locate the database
DB_PATH = Path(__file__).resolve().parent / "campus_connect.db"

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# Display all tables
print("\n========== DATABASE TABLES ==========")

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    AND name NOT LIKE 'sqlite_%'
""")

tables = cursor.fetchall()

for table in tables:
    table_name = table["name"]

    print(f"\n\n========== {table_name} TABLE ==========")

    # Display column information
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    print("\nColumns:")
    for column in columns:
        print(
            f"{column['name']} | "
            f"Type: {column['type']} | "
            f"Primary Key: {column['pk']}"
        )

    # Display all records
    cursor.execute(f'SELECT * FROM "{table_name}"')
    records = cursor.fetchall()

    print("\nSaved Records:")

    if records:
        for record in records:
            print(dict(record))
    else:
        print("No records found.")

print("\n========== END OF DATABASE ==========")

conn.close()
