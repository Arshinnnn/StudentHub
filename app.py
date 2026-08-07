from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/notes")
def notes():
    return render_template("notes.html")

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
