from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "studenthub.db")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Notes
    cursor.execute("SELECT COUNT(*) FROM notes")
    total_notes = cursor.fetchone()[0]

    # Tasks
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
    completed_tasks = cursor.fetchone()[0]

    pending_tasks = total_tasks - completed_tasks

    # Expenses
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0

    connection.close()

    return render_template(
        "dashboard.html",
        total_notes=total_notes,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        total_expenses=total_expenses
    )


@app.route("/notes", methods=["GET", "POST"])
def notes():
    connection = sqlite3.connect("DATABASE")
    cursor = connection.cursor()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title, content)
        )

        connection.commit()

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    connection.close()

    return render_template("notes.html", notes=notes)


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


@app.route("/edit_note/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        cursor.execute(
            "UPDATE notes SET title = ?, content = ? WHERE id = ?",
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

    return render_template("edit_note.html", note=note)


@app.route("/planner", methods=["GET", "POST"])
def planner():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        priority = request.form["priority"]

        cursor.execute(
            "INSERT INTO tasks (title, priority) VALUES (?, ?)",
            (title, priority)
        )

        connection.commit()

    cursor.execute(
        "SELECT * FROM tasks ORDER BY completed ASC, id DESC"
    )

    tasks = cursor.fetchall()

    connection.close()

    return render_template("planner.html", tasks=tasks)

@app.route("/expenses", methods=["GET", "POST"])
def expenses():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]

        cursor.execute(
            "INSERT INTO expenses (title, amount) VALUES (?, ?)",
            (title, amount)
        )

        connection.commit()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    total = sum(expense[2] for expense in expenses)

    connection.close()

    return render_template(
        "expenses.html",
        expenses=expenses,
        total=total
    )

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)