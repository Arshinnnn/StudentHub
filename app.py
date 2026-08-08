from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/notes", methods=["GET", "POST"])
def notes():
    connection = sqlite3.connect("studenthub.db")
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
    connection = sqlite3.connect("studenthub.db")
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
    connection = sqlite3.connect("studenthub.db")
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


@app.route("/planner")
def planner():
    return render_template("planner.html")


@app.route("/expenses")
def expenses():
    return render_template("expenses.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)