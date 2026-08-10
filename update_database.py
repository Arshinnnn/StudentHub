import sqlite3

connection = sqlite3.connect("studenthub.db")
cursor = connection.cursor()

try:
    cursor.execute(
        "ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'"
    )
    connection.commit()
    print("Priority column added!")
except sqlite3.OperationalError:
    print("Priority column already exists.")

connection.close()