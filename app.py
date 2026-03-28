from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

# ✅ INIT DATABASE
def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Student(
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        dept TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Course(
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        credits INTEGER
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Marks(
        student_id INTEGER,
        course_id INTEGER,
        marks INTEGER,
        grade TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS Enrollment(
        student_id INTEGER,
        course_id INTEGER,
        PRIMARY KEY(student_id, course_id)
    )
    """)

    conn.commit()
    conn.close()

init_db()

# 🔐 LOGIN CHECK
def is_logged_in():
    return "user" in session

# HOME
@app.route("/")
def index():
    if not is_logged_in():
        return redirect("/login")

    conn = get_db()
    students = conn.execute("SELECT * FROM Student").fetchall()
    conn.close()

    return render_template("index.html", students=students)

# ADD STUDENT
@app.route("/add", methods=["POST"])
def add():
    if not is_logged_in():
        return redirect("/login")

    conn = get_db()
    conn.execute(
        "INSERT INTO Student (name,email,phone,dept) VALUES (?,?,?,?)",
        (
            request.form["name"],
            request.form["email"],
            request.form["phone"],
            request.form["dept"]
        )
    )
    conn.commit()
    conn.close()
    return redirect("/")

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    if not is_logged_in():
        return redirect("/login")

    conn = get_db()
    conn.execute("DELETE FROM Student WHERE student_id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# UPDATE
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if not is_logged_in():
        return redirect("/login")

    conn = get_db()
    conn.execute("""
        UPDATE Student 
        SET name=?, email=?, phone=?, dept=? 
        WHERE student_id=?
    """, (
        request.form["name"],
        request.form["email"],
        request.form["phone"],
        request.form["dept"],
        id
    ))
    conn.commit()
    conn.close()
    return redirect("/")

# COURSES
@app.route("/courses")
def courses():
    if not is_logged_in():
        return redirect("/login")

    conn = get_db()
    courses = conn.execute("SELECT * FROM Course").fetchall()
    conn.close()

    return render_template("courses.html", courses=courses)

# ADD COURSE
@app.route("/add_course", methods=["POST"])
def add_course():
    if not is_logged_in():
        return redirect("/login")

    conn = get_db()
    conn.execute(
        "INSERT INTO Course(course_name, credits) VALUES (?,?)",
        (request.form["name"], request.form["credits"])
    )
    conn.commit()
    conn.close()
    return redirect("/courses")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM Users WHERE username=? AND password=?",
            (request.form["username"], request.form["password"])
        ).fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html", error="Invalid credentials")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        # ✅ check if user exists
        existing = conn.execute(
            "SELECT * FROM Users WHERE username=?",
            (username,)
        ).fetchone()

        if existing:
            return render_template("register.html", error="Username already exists")

        conn.execute(
            "INSERT INTO Users(username,password) VALUES (?,?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect("/login")

    conn = get_db()
    total_students = conn.execute("SELECT COUNT(*) FROM Student").fetchone()[0]
    total_courses = conn.execute("SELECT COUNT(*) FROM Course").fetchone()[0]
    conn.close()

    return render_template("dashboard.html",
                           students=total_students,
                           courses=total_courses)                          
                           
# ENROLL
@app.route("/enroll", methods=["POST"])
def enroll():
    if not is_logged_in():
        return redirect("/login")

    conn = get_db()
    conn.execute(
        "INSERT INTO Enrollment VALUES (?,?)",
        (request.form["student_id"], request.form["course_id"])
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/report")
def report():
    if not is_logged_in():
        return redirect("/login")

    conn = get_db()

    data = conn.execute("""
        SELECT Student.name, Course.course_name, Marks.marks, Marks.grade
        FROM Marks
        JOIN Student ON Marks.student_id = Student.student_id
        JOIN Course ON Marks.course_id = Course.course_id
    """).fetchall()

    conn.close()

    return render_template(
    "dashboard.html",
    students=10,
    courses=5
)

if __name__ == "__main__":
    app.run(debug=True)