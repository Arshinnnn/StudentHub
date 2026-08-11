import sqlite3

connection = sqlite3.connect("studenthub.db")
cursor = connection.cursor()

# Add priority column
try:
    cursor.execute(
        "ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'"
    )
    print("Priority column added!")
except sqlite3.OperationalError:
    print("Priority column already exists.")

# Add due date column
try:
    cursor.execute(
        "ALTER TABLE tasks ADD COLUMN due_date TEXT"
    )
    print("Due date column added!")
except sqlite3.OperationalError:
    print("Due date column already exists.")

connection.commit()
connection.close()

print("Database update complete!")