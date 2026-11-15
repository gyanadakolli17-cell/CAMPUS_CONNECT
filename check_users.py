import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / "campus_connect.db"

conn = sqlite3.connect(db_path)

users = conn.execute("""
    SELECT user_id, full_name, email, department, year
    FROM Users
""").fetchall()

print("REGISTERED STUDENTS:")
for user in users:
    print(user)

conn.close()