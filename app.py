
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

app = Flask(__name__)

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
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Answers (
            answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id)
                REFERENCES Questions(question_id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return redirect(url_for("questions"))


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


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
