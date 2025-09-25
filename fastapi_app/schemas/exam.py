from pydantic import BaseModel
from datetime import date

class ExamCreate(BaseModel):
    name: str
    date: date
    course_code: str

class ExamOut(BaseModel):
    id: int
    name: str
    date: date
    course_code: str

    class Config:
        from_attributes = True

class ResultsIn(BaseModel):
    results: dict  # {student_roll_no: score}
