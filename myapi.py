from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# C - Create (POST)
# R - Read  (GET)
# U - Update (PUT)
# D - Delete (DELETE)

students = {
    1: {
        'name': 'john',
        'age': 17,
        'year': 12,
    },
    2: {
        'name': 'rohan',
        'age': 27,
        'year': 'graduate',
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get('/')
def index():
    return students;

# Path parameters
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description="The ID of the student you want to view", gt=0)):
    return students[student_id]

# Query parameter

@app.get('/get-by-name')
def get_student(*, name: Optional[str] = None, tests: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]

    return { "Data": "Not found"}

# request body

@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if(student_id in students):
        return { "error": "student exists with this id"}
    
    students[student_id] = student
    return students[student_id]

@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: UpdateStudent):
    if(student_id not in students):
        return {'error':'student does not exist'}
    
    if(student.name != None):
        students[student_id].name = student.name

    if(student.age != None):
        students[student_id].age = student.age

    if(student.year != None):
        students[student_id].year = student.year

    return students[student_id]

@app.delete('/delete-student/{student_id}')
def delete_student(student_id: int):
    if student_id not in students:
        return { 'error': 'student does not exists'}

    del students[student_id]
    return { 'msg': 'student deleted successfully' }

# server command => uvicorn myapi:app --reload