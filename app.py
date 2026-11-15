
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "campus-connect-local-development-key"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "campus_connect.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Answers (
            answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            FOREIGN KEY (question_id)
                REFERENCES Questions(question_id)
                ON DELETE CASCADE
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/information")
def information():
    return render_template("information.html")


@app.route("/ask-seniors")
def ask_seniors():
    return render_template("ask-seniors.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/seniors")
def seniors():
    return render_template("seniors.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # 1. Get the submitted email and password
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # 2. Check whether both fields are filled
        if not email or not password:
            return render_template(
                "login.html",
                error="Please enter your email and password."
            )

        # 3. Find the student using their email
        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM Users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        # 4. Check the password against the stored hash
        if user and check_password_hash(user["password_hash"], password):

            # 5. Remember that the student is logged in
            session["user_id"] = user["user_id"]
            session["user_name"] = user["full_name"]

            return redirect(url_for("home"))

        # 6. Incorrect login details
        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # 1. Collect form data
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        department = request.form.get("department", "").strip()
        year = request.form.get("year", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # 2. Check that all fields are filled
        if not all([full_name, email, department, year,
                    password, confirm_password]):
            return render_template(
                "register.html",
                error="Please fill in all fields."
            )

        # 3. Check password length
        if len(password) < 8:
            return render_template(
                "register.html",
                error="Password must contain at least 8 characters."
            )

        # 4. Check whether passwords match
        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        # 5. Hash the password
        password_hash = generate_password_hash(password)

        # 6. Store the student in the database
        conn = get_db_connection()

        try:
            conn.execute(
                """INSERT INTO Users
                (full_name, email, department, year, password_hash)
                VALUES (?, ?, ?, ?, ?)""",
                (full_name, email, department, year, password_hash)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return render_template(
                "register.html",
                error="This email is already registered."
            )

        conn.close()

        # 7. Registration successful
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/questions", methods=["GET", "POST"])
def questions():

    if request.method == "POST":
        question_text = request.form.get("question_text", "").strip()
        category = request.form.get("category", "").strip()

        allowed_categories = ["General", "Academics", "Placements"]

        if question_text and category in allowed_categories:
            conn = get_db_connection()

            conn.execute(
                """INSERT INTO Questions
                (question_text, category)
                VALUES (?, ?)""",
                (question_text, category)
            )

            conn.commit()
            conn.close()

        return redirect(url_for("questions"))

    conn = get_db_connection()

    selected_category = request.args.get("category", "").strip()

    allowed_categories = ["General", "Academics", "Placements"]

    if selected_category in allowed_categories:
        questions = conn.execute(
            "SELECT * FROM Questions WHERE category = ? ORDER BY question_id DESC",
            (selected_category,)
        ).fetchall()
    else:
        selected_category = ""

        questions = conn.execute(
            "SELECT * FROM Questions ORDER BY question_id DESC"
        ).fetchall()

    answers_by_question = {}

    for q in questions:
        answers_by_question[q["question_id"]] = conn.execute(
            "SELECT * FROM Answers WHERE question_id = ? ORDER BY answer_id ASC",
            (q["question_id"],)
        ).fetchall()

    conn.close()

    return render_template(
        "questions.html",
        questions=questions,
        answers_by_question=answers_by_question,
        selected_category=selected_category
    )


@app.route("/answer/<int:question_id>", methods=["POST"])
def submit_answer(question_id):

    answer_text = request.form.get("answer_text", "").strip()

    if answer_text:
        conn = get_db_connection()

        # Check whether the question exists
        question = conn.execute(
            "SELECT question_id FROM Questions WHERE question_id = ?",
            (question_id,)
        ).fetchone()

        if question:
            conn.execute(
                """INSERT INTO Answers (question_id, answer_text)
                VALUES (?, ?)""",
                (question_id, answer_text)
            )

            conn.commit()

        conn.close()

    return redirect(url_for("questions"))


create_tables()

if __name__ == "__main__":
    app.run(debug=True)
