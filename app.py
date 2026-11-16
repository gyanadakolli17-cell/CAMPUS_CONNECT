
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            visual_class TEXT NOT NULL,
            visual_label TEXT NOT NULL,
            tag_label TEXT NOT NULL,
            availability TEXT NOT NULL,
            description TEXT NOT NULL,
            tech_stack TEXT NOT NULL,
            roles_needed TEXT NOT NULL,
            lead_info TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS ProjectInterests (
            interest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            student_email TEXT NOT NULL,
            contribution TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id)
                REFERENCES Projects(project_id)
                ON DELETE CASCADE
        )
    """)

    # NEW TABLE: Seniors
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Seniors (
            senior_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            department_name TEXT NOT NULL,
            year TEXT NOT NULL,
            initials TEXT NOT NULL,
            avatar_class TEXT NOT NULL,
            bio TEXT NOT NULL,
            topic TEXT NOT NULL,
            tags TEXT NOT NULL,
            availability TEXT NOT NULL,
            response_time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
def insert_sample_projects():

    conn = get_db_connection()

    projects = [
        (
            "VR Lab Simulator (Team xANDER)",
            "design",
            "visual-purple",
            "AR/VR & AI/ML",
            "AR/VR & AI/ML",
            "Open for 1st/2nd Year",
            "An immersive virtual reality laboratory simulator designed to improve accessibility, safety, and hands-on learning for engineering experiments without physical lab hazards.",
            "Unity, C#, Blender, OpenXR, Python",
            "Looking for 2 helpers in 3D asset modeling and UI/UX testing.",
            "Leads: Mujawar Zaid, Deepthi Buchupalli & Samarth Pasalkar (AIML — 1st Prize, INNOVATEX 4.0)"
        ),
        (
            "Authentix — Smart IoT Security & Verification System",
            "social",
            "visual-green",
            "IOT / HARDWARE",
            "IoT / Hardware & AI/ML",
            "2 Spots Available",
            "A hardware-software integrated authentication solution built to prevent unauthorized access and tampering in connected environments.",
            "Python, Embedded C, Arduino/ESP32, MQTT, Machine Learning",
            "Seeking juniors interested in sensor integration and backend dashboard development.",
            "Leads: Milan, Ashutosh Sharma, Talha & Aryan R (CSE & AIML — IoT Track Winners, NMH Hacks)"
        ),
        (
            "CyberShield — Interactive Phishing Defense Simulator",
            "web",
            "visual-orange",
            "CYBERSECURITY & WEB",
            "Cybersecurity & Web Dev",
            "Open for 2nd Year",
            "An interactive training platform that educates students and users on cyber hygiene through simulated phishing scenarios.",
            "Python, React, Node.js, NLP, HTML/CSS",
            "Looking for 1 Frontend Helper to build interactive scenario cards.",
            "Leads: Richard U, M. Jeethendra Reddy, Shashank G & Y. Uday Kumar (CSE — InCSEption 2.0 Winners)"
        ),
        (
            "CyberGuard-AI — Explainable Threat Detection System",
            "ai",
            "visual-blue",
            "AI/ML & CLOUD",
            "AI/ML & Cloud Security",
            "Open for 2nd/3rd Year",
            "Uses Graph Neural Networks (GNNs) to detect cyberattacks across IoT and cloud networks while providing human-readable explanations.",
            "Python, PyTorch Geometric (GNNs), Docker, Cloud APIs, Explainable AI",
            "Looking for 1 backend or React helper to build a live alert dashboard.",
            "Lead: Sindhu C — CS Postgrad, BMSIT&M"
        ),
        (
            "High-Speed Multilingual SMS & Threat Classifier",
            "ai",
            "visual-purple",
            "AI/ML & NLP",
            "AI/ML & NLP",
            "2 Spots Available",
            "A transformer-based classification pipeline designed to filter multilingual messages.",
            "Python, Hugging Face Transformers, PyTorch, FastAPI, ONNX",
            "Seeking juniors interested in dataset annotation and model optimization.",
            "Lead: Manas Khanna — 4th Year AIML ('27), BMSIT&M"
        )
    ]

    for project in projects:
        conn.execute(
            """INSERT OR IGNORE INTO Projects
            (title, category, visual_class, visual_label,
             tag_label, availability, description, tech_stack,
             roles_needed, lead_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            project
        )

    conn.commit()
    conn.close()

def insert_sample_seniors():
    conn = get_db_connection()

    seniors = [
        (
            "Neha Rao", "cse", "Computer Science", "4th Year",
            "NR", "avatar-blue",
            "I enjoy helping juniors with web development, hackathons and building portfolios.",
            "software", "Web development,Hackathons",
            "Open to questions", "Usually replies in a day"
        ),
        (
            "Arjun Mehta", "ise", "Information Science", "4th Year",
            "AM", "avatar-purple",
            "I can help with machine learning, data basics and presenting technical work.",
            "data", "Machine learning,Python",
            "Open to questions", "Usually replies in a day"
        ),
        (
            "Aisha Khan", "ece", "Electronics & Communication", "4th Year",
            "AK", "avatar-teal",
            "I can guide juniors with electronics coursework, internships and career paths.",
            "career", "Internships,Career planning",
            "Open to questions", "Usually replies in 2 days"
        ),
        (
            "Rohan Shetty", "cse", "Computer Science", "3rd Year",
            "RS", "avatar-orange",
            "I enjoy UI design, product thinking and helping students build prototypes.",
            "design", "UI / UX,Product design",
            "Open to questions", "Usually replies in a day"
        ),
        (
            "Kavya Nair", "me", "Mechanical Engineering", "4th Year",
            "KN", "avatar-rose",
            "I can help juniors explore student teams, design competitions and hands-on opportunities.",
            "career", "Design teams,Opportunities",
            "Open to questions", "Usually replies in 2 days"
        ),
        (
            "Dev Patel", "eee", "Electrical & Electronics", "4th Year",
            "DP", "avatar-green",
            "I enjoy explaining embedded systems, beginner coding projects and getting started with your first build.",
            "software", "Embedded systems,C programming",
            "Open to questions", "Usually replies in a day"
        )
    ]

    for senior in seniors:
        conn.execute(
            """INSERT OR IGNORE INTO Seniors
            (full_name, department, department_name, year,
             initials, avatar_class, bio, topic, tags,
             availability, response_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            senior
        )

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/information")
def information():
    return render_template("information.html")


@app.route("/ask-seniors")
def ask_seniors():
    return render_template("ask-seniors.html")


@app.route("/projects")
def projects():
    conn = get_db_connection()

    projects = conn.execute(
        "SELECT * FROM Projects ORDER BY project_id"
    ).fetchall()

    conn.close()

    return render_template("projects.html", projects=projects)

@app.route("/project-interest", methods=["POST"])
def project_interest():

    student_name = request.form.get("name", "").strip()
    student_email = request.form.get("email", "").strip()
    contribution = request.form.get("message", "").strip()
    project_id = request.form.get("project_id", "").strip()

    # Validate the submitted information
    if not student_name or not student_email or len(student_name) > 80:
        return "Please enter a valid name and email.", 400

    if "@" not in student_email or len(student_email) > 254:
        return "Please enter a valid email address.", 400

    if not contribution or len(contribution) < 10 or len(contribution) > 400:
        return "Contribution message must be between 10 and 400 characters.", 400

    if not project_id:
        return "Please select a project.", 400

    try:
        project_id = int(project_id)
    except ValueError:
        return "Invalid project selection.", 400

    conn = get_db_connection()

    project = conn.execute(
        "SELECT project_id FROM Projects WHERE project_id = ?",
        (project_id,)
    ).fetchone()

    if project is None:
        conn.close()
        return "Selected project does not exist.", 404

    conn.execute(
        """INSERT INTO ProjectInterests
        (project_id, student_name, student_email, contribution)
        VALUES (?, ?, ?, ?)""",
        (project_id, student_name, student_email, contribution)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("projects"))

@app.route("/seniors")
def seniors():
    conn = get_db_connection()

    seniors = conn.execute(
        "SELECT * FROM Seniors ORDER BY senior_id"
    ).fetchall()

    conn.close()

    return render_template("seniors.html", seniors=seniors)

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
insert_sample_projects()
insert_sample_seniors()

if __name__ == "__main__":
    app.run(debug=True)
