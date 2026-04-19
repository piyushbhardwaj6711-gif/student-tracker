from __future__ import annotations

import json
import os
import re
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import Integer, String, create_engine, inspect, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

_BASE_DIR = Path(__file__).resolve().parent
load_dotenv(_BASE_DIR / ".env")
load_dotenv(_BASE_DIR / "student tracker.env")

JSON_PATH = _BASE_DIR / "students.json"
_DEFAULT_DB = "student_db"

_engine = None


def _settings() -> dict:
    return {
        "host": os.environ.get("MYSQL_HOST", "127.0.0.1"),
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", ""),
        "port": int(os.environ.get("MYSQL_PORT", "3306")),
        "database": os.environ.get("MYSQL_DATABASE", _DEFAULT_DB),
    }


def _safe_db_name(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_]+", name):
        raise ValueError(
            "MYSQL_DATABASE must contain only letters, digits, and underscores."
        )
    return name


def _mysql_url(*, database: str | None) -> str:
    s = _settings()
    user = quote_plus(s["user"])
    password = quote_plus(s["password"])
    host = s["host"]
    port = s["port"]
    path = f"/{database}" if database else ""
    return f"mysql+pymysql://{user}:{password}@{host}:{port}{path}?charset=utf8mb4"


def _ensure_database() -> None:
    db = _safe_db_name(_settings()["database"])
    admin_engine = create_engine(
        _mysql_url(database=None),
        isolation_level="AUTOCOMMIT",
    )
    try:
        with admin_engine.connect() as conn:
            conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{db}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
    finally:
        admin_engine.dispose()


def get_engine():
    global _engine
    if _engine is None:
        _ensure_database()
        _engine = create_engine(
            _mysql_url(database=_settings()["database"]),
            pool_pre_ping=True,
        )
    return _engine


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    course: Mapped[str] = mapped_column(String(500), nullable=False, server_default="")


_session_factory = sessionmaker(autoflush=False, expire_on_commit=False)


def _session():
    return _session_factory(bind=get_engine())


def init_db():
    Base.metadata.create_all(bind=get_engine())
    seed_from_json()


def _student_column_names() -> set[str]:
    eng = get_engine()
    insp = inspect(eng)
    if not insp.has_table("students"):
        return set()
    return {c["name"].lower() for c in insp.get_columns("students")}


def _default_email(student_id: str) -> str:
    sid = str(student_id).strip()
    if not sid:
        sid = "unknown"
    return f"{sid}@student.local"


def seed_from_json():
    if not JSON_PATH.exists():
        return

    with JSON_PATH.open("r", encoding="utf-8") as f:
        try:
            payload = json.load(f)
        except json.JSONDecodeError:
            return

    if not isinstance(payload, list):
        return

    columns = _student_column_names()
    if not columns:
        return

    eng = get_engine()
    with eng.begin() as conn:
        if "email" in columns:
            stmt = text(
                """
                INSERT IGNORE INTO students (id, name, age, course, email)
                VALUES (:id, :name, :age, :course, :email)
                """
            )
            for s in payload:
                sid = str(s.get("id", ""))
                if not sid:
                    continue
                conn.execute(
                    stmt,
                    {
                        "id": sid,
                        "name": s.get("name", ""),
                        "age": int(s.get("age", 0) or 0),
                        "course": s.get("course", ""),
                        "email": _default_email(sid),
                    },
                )
        else:
            stmt = text(
                """
                INSERT IGNORE INTO students (id, name, age, course)
                VALUES (:id, :name, :age, :course)
                """
            )
            for s in payload:
                sid = str(s.get("id", ""))
                if not sid:
                    continue
                conn.execute(
                    stmt,
                    {
                        "id": sid,
                        "name": s.get("name", ""),
                        "age": int(s.get("age", 0) or 0),
                        "course": s.get("course", ""),
                    },
                )


def load_students():
    seed_from_json()
    session = _session()
    try:
        rows = session.scalars(select(Student)).all()
        return [
            {"id": r.id, "name": r.name, "age": r.age, "course": r.course} for r in rows
        ]
    finally:
        session.close()


def add_student(student_id, name, age, course):
    columns = _student_column_names()
    session = _session()
    try:
        if "email" in columns:
            session.execute(
                text(
                    """
                    INSERT INTO students (id, name, age, course, email)
                    VALUES (:id, :name, :age, :course, :email)
                    """
                ),
                {
                    "id": student_id,
                    "name": name,
                    "age": age,
                    "course": course,
                    "email": _default_email(str(student_id)),
                },
            )
        else:
            session.add(
                Student(id=str(student_id), name=name, age=int(age), course=course)
            )
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def update_student(student_id, name, age, course):
    session = _session()
    try:
        session.execute(
            text(
                "UPDATE students SET name=:name, age=:age, course=:course WHERE id=:id"
            ),
            {
                "name": name,
                "age": int(age),
                "course": course,
                "id": student_id,
            },
        )
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_student(student_id):
    session = _session()
    try:
        row = session.get(Student, student_id)
        if row is not None:
            session.delete(row)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


init_db()
