import sqlite3
import csv

connection = sqlite3.connect("vacancies.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        salary TEXT,
        area_name TEXT,
        published_at TEXT
    )
""")

with open("vacancies_preprocessed_100.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute("""
            INSERT INTO vacancies (name, salary, area_name, published_at)
            VALUES (?, ?, ?, ?) 
        """, (
            row["name"],
            row["salary"],
            row["area_name"],
            row["published_at"]
        ))

connection.commit()