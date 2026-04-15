import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("students.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout = 10000")
    return conn


def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER DEFAULT 0,
                course TEXT DEFAULT ''
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def _get_student_columns(cursor):
    cursor.execute("PRAGMA table_info(students)")
    return {row["name"] for row in cursor.fetchall()}


def load_students():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def add_student(student_id, name, age, course):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        columns = _get_student_columns(cursor)
        if "email" in columns:
            # Compatibility with older schema where email is NOT NULL.
            query = "INSERT INTO students (id, name, age, course, email) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (student_id, name, age, course, ""))
        else:
            query = "INSERT INTO students (id, name, age, course) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (student_id, name, age, course))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_student(student_id, name, age, course):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        query = "UPDATE students SET name=?, age=?, course=? WHERE id=?"
        cursor.execute(query, (name, age, course, student_id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_student(student_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        query = "DELETE FROM students WHERE id=?"
        cursor.execute(query, (student_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


init_db()