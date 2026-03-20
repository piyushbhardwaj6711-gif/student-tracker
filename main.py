from fastapi import FastAPI
from data import load_students

app = FastAPI()

@app.get("/")
def root():
    return {"message": "backend running"}

@app.get("/students")
def get_students():
    return load_students()