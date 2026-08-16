from flask import Flask, render_template, request, redirect
import sqlite3
import os
from datetime import date


app = Flask(__name__)

# Always use the database inside the StudentHub folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "studenthub.db")


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Total notes
    cursor.execute("SELECT COUNT(*) FROM notes")
    total_notes = cursor.fetchone()[0]

    # Total tasks
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    # Completed tasks
    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 1"
    )
    completed_tasks = cursor.fetchone()[0]

    # Pending tasks
    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE completed = 0"
    )
    pending_tasks = cursor.fetchone()[0]

    # Total expenses
    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    )
    total_expenses = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "dashboard.html",
        total_notes=total_notes,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        total_expenses=total_expenses
    )


# --------------------------------------------------
# NOTES
# --------------------------------------------------
# --------------------------------------------------
# NOTES
# --------------------------------------------------

@app.route("/notes", methods=["GET", "POST"])
def notes():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        cursor.execute(
            """
            INSERT INTO notes (title, content)
            VALUES (?, ?)
            """,
            (title, content)
        )

        connection.commit()

    search = request.args.get("search", "").strip()

    if search:

        cursor.execute(
            """
            SELECT * FROM notes
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY id DESC
            """,
            (f"%{search}%", f"%{search}%")
        )

    else:

        cursor.execute(
            "SELECT * FROM notes ORDER BY id DESC"
        )

    notes = cursor.fetchall()

    connection.close()

    return render_template(
        "notes.html",
        notes=notes,
        search=search
    )


# --------------------------------------------------
# EDIT NOTE
# --------------------------------------------------

@app.route("/edit_note/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        cursor.execute(
            """
            UPDATE notes
            SET title = ?, content = ?
            WHERE id = ?
            """,
            (title, content, note_id)
        )

        connection.commit()
        connection.close()

        return redirect("/notes")

    cursor.execute(
        "SELECT * FROM notes WHERE id = ?",
        (note_id,)
    )

    note = cursor.fetchone()

    connection.close()

    return render_template(
        "edit_note.html",
        note=note
    )


# --------------------------------------------------
# DELETE NOTE
# --------------------------------------------------

@app.route("/delete_note/<int:note_id>")
def delete_note(note_id):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/notes")


# --------------------------------------------------
# PLANNER
# --------------------------------------------------

@app.route("/planner", methods=["GET", "POST"])
def planner():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]

        cursor.execute(
            """
            INSERT INTO tasks
            (title, completed, priority, due_date)
            VALUES (?, 0, ?, ?)
            """,
            (title, priority, due_date)
        )

        connection.commit()

    # -----------------------------
    # TASK STATISTICS
    # -----------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM tasks"
    )
    total_tasks = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE completed = 1
        """
    )
    completed_tasks = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE completed = 0
        """
    )
    pending_tasks = cursor.fetchone()[0]

    today = date.today().isoformat()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE completed = 0
        AND due_date < ?
        """,
        (today,)
    )
    overdue_tasks = cursor.fetchone()[0]

    # -----------------------------
    # TASK FILTER
    # -----------------------------

    status = request.args.get("status", "all")

    if status == "pending":

        cursor.execute(
            """
            SELECT *
            FROM tasks
            WHERE completed = 0
            ORDER BY due_date ASC
            """
        )

    elif status == "completed":

        cursor.execute(
            """
            SELECT *
            FROM tasks
            WHERE completed = 1
            ORDER BY due_date DESC
            """
        )

    else:

        cursor.execute(
            """
            SELECT *
            FROM tasks
            ORDER BY completed ASC, due_date ASC
            """
        )

    tasks = cursor.fetchall()

    connection.close()

    return render_template(
        "planner.html",
        tasks=tasks,
        today=today,
        status=status,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks
    )

# --------------------------------------------------
# EXPENSES
# --------------------------------------------------

@app.route("/expenses", methods=["GET", "POST"])
def expenses():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]

        cursor.execute(
            """
            INSERT INTO expenses (title, amount)
            VALUES (?, ?)
            """,
            (title, amount)
        )

        connection.commit()

    cursor.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    )

    expenses = cursor.fetchall()

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    )

    total_expenses = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "expenses.html",
        expenses=expenses,
        total_expenses=total_expenses
    )


# --------------------------------------------------
# ABOUT
# --------------------------------------------------

@app.route("/about")
def about():
    return render_template("about.html")


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)