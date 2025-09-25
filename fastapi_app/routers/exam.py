from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.exam import Exam
from ..schemas.exam import ExamCreate, ExamOut, ResultsIn
from ..auth import get_current_user
from ..redis_cache import cache_get, cache_set
import json

router = APIRouter()

@router.post("/exams", response_model=ExamOut)
def create_exam(payload: ExamCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    e = Exam(name=payload.name, date=payload.date, course_code=payload.course_code)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e

@router.post("/exams/results")
def bulk_results(payload: ResultsIn, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    # Store results as JSON string in the most recent exam for a course (demo purpose).
    exam = db.query(Exam).order_by(Exam.id.desc()).first()
    if not exam:
        raise HTTPException(status_code=400, detail="No exams to attach results")
    exam.results_json = json.dumps(payload.results)
    db.commit()
    return {"ok": True, "exam_id": exam.id}

@router.get("/timetable/{student_roll}")
def cached_timetable(student_roll: str, user: str = Depends(get_current_user)):
    cache_key = f"timetable:{student_roll}"
    cached = cache_get(cache_key)
    if cached:
        return {"cached": True, "data": json.loads(cached)}
    # Demo: construct a pseudo timetable
    data = {
        "student": student_roll,
        "slots": [
            {"day": "Mon", "9:00": "CS101", "11:00": "MA201"},
            {"day": "Wed", "10:00": "CS101 Lab"},
            {"day": "Fri", "9:00": "PH102"}
        ]
    }
    cache_set(cache_key, data, ttl=600)
    return {"cached": False, "data": data}
