import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "students.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                student_class TEXT NOT NULL,
                attendance REAL NOT NULL,
                study_hours REAL NOT NULL,
                previous_marks REAL NOT NULL,
                final_marks REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def add_student(student_id, name, student_class,
                attendance, study_hours,
                previous_marks, final_marks):

    if not student_id.strip() or not name.strip():
        raise ValueError("Student ID and name are required.")

    if not 0 <= attendance <= 100:
        raise ValueError("Attendance must be between 0 and 100.")

    if study_hours < 0 or study_hours > 24:
        raise ValueError("Study hours must be between 0 and 24.")

    if not 0 <= previous_marks <= 100:
        raise ValueError("Previous marks must be between 0 and 100.")

    if not 0 <= final_marks <= 100:
        raise ValueError("Final marks must be between 0 and 100.")

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO students (
                student_id, name, student_class,
                attendance, study_hours,
                previous_marks, final_marks, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id.strip(),
            name.strip(),
            student_class.strip(),
            attendance,
            study_hours,
            previous_marks,
            final_marks,
            created_at
        ))


def get_students(search=""):
    search = search.strip()

    with get_connection() as conn:
        return conn.execute("""
            SELECT *
            FROM students
            WHERE student_id LIKE ? OR name LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%")).fetchall()


def update_student(student_id, name, student_class,
                   attendance, study_hours,
                   previous_marks, final_marks):

    if not name.strip() or not student_class.strip():
        raise ValueError("Name and class are required.")

    if not 0 <= attendance <= 100:
        raise ValueError("Attendance must be between 0 and 100.")

    if not 0 <= study_hours <= 24:
        raise ValueError("Study hours must be between 0 and 24.")

    if not 0 <= previous_marks <= 100:
        raise ValueError("Previous marks must be between 0 and 100.")

    if not 0 <= final_marks <= 100:
        raise ValueError("Final marks must be between 0 and 100.")

    with get_connection() as conn:
        cursor = conn.execute("""
            UPDATE students
            SET name = ?,
                student_class = ?,
                attendance = ?,
                study_hours = ?,
                previous_marks = ?,
                final_marks = ?
            WHERE student_id = ?
        """, (
            name.strip(),
            student_class.strip(),
            attendance,
            study_hours,
            previous_marks,
            final_marks,
            student_id
        ))

        if cursor.rowcount == 0:
            raise ValueError("Student not found.")


def delete_student(student_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )

        if cursor.rowcount == 0:
            raise ValueError("Student not found.")


def get_dashboard_stats():
    with get_connection() as conn:
        result = conn.execute("""
            SELECT
                COUNT(*) AS total_students,
                COALESCE(AVG(final_marks), 0) AS average_marks,
                COALESCE(AVG(attendance), 0) AS average_attendance
            FROM students
        """).fetchone()

        return {
            "total_students": result["total_students"],
            "average_marks": result["average_marks"],
            "average_attendance": result["average_attendance"]
        }


if __name__ == "__main__":
    initialize_database()
    print("Student database created successfully!")