from fastapi import FastAPI
from pydantic import BaseModel
from data import load_students, add_student, update_student, delete_student

app = FastAPI()


class Student(BaseModel):
    id: str
    name: str
    age: int
    course: str


@app.get("/")
def root():
    return {"message": "backend running"}


@app.get("/students")
def get_students():
    return load_students()


@app.post("/students")
def create_student(student: Student):
    add_student(student.id, student.name, student.age, student.course)
    return {"message": "Student added successfully"}


@app.put("/students/{student_id}")
def edit_student(student_id: str, student: Student):
    update_student(student_id, student.name, student.age, student.course)
    return {"message": "Student updated successfully"}


@app.delete("/students/{student_id}")
def remove_student(student_id: str):
    delete_student(student_id)
    return {"message": "Student deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)