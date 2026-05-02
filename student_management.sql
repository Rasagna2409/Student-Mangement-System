-- 🔹 ENABLE FOREIGN KEYS (IMPORTANT IN SQLITE)
PRAGMA foreign_keys = ON;

-- 🔹 STUDENT TABLE
CREATE TABLE IF NOT EXISTS Student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    dept TEXT NOT NULL
);

-- 🔹 COURSE TABLE
CREATE TABLE IF NOT EXISTS Course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL UNIQUE,
    credits INTEGER CHECK(credits > 0)
);

-- 🔹 USERS (LOGIN)
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- 🔹 ENROLLMENT (MANY-TO-MANY)
CREATE TABLE IF NOT EXISTS Enrollment (
    student_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY(student_id, course_id),
    
    FOREIGN KEY(student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY(course_id) REFERENCES Course(course_id) ON DELETE CASCADE
);

-- 🔹 MARKS
CREATE TABLE IF NOT EXISTS Marks (
    student_id INTEGER,
    course_id INTEGER,
    marks INTEGER CHECK(marks BETWEEN 0 AND 100),
    grade TEXT,

    PRIMARY KEY(student_id, course_id),

    FOREIGN KEY(student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY(course_id) REFERENCES Course(course_id) ON DELETE CASCADE
);