from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.student import Student
from ..models.course import Course
from ..models.associations import StudentCourse
from ..schemas.student import StudentCreate, StudentOut
from ..auth import get_current_user

router = APIRouter()

@router.post("/students", response_model=StudentOut)
def create_student(payload: StudentCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    s = Student(name=payload.name, roll_no=payload.roll_no, email=payload.email)
    db.add(s)
    try:
        db.commit()
        db.refresh(s)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate roll_no or email")
    return s

@router.get("/students/{sid}", response_model=StudentOut)
def get_student(sid: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    s = db.get(Student, sid)
    if not s:
        raise HTTPException(status_code=404, detail="Student not found")
    return s

@router.get("/students")
def list_students(limit: int = Query(20, ge=1, le=200), offset: int = Query(0, ge=0), q: str | None = None,
                  db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    query = db.query(Student)
    if q:
        like = f"%{q}%"
        query = query.filter((Student.name.ilike(like)) | (Student.roll_no.ilike(like)) | (Student.email.ilike(like)))
    total = query.count()
    items = query.order_by(Student.id).limit(limit).offset(offset).all()
    return {"total": total, "items": items}

@router.post("/students/{sid}/enroll/{course_id}")
def enroll_student(sid: int, course_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    s = db.get(Student, sid)
    c = db.get(Course, course_id)
    if not s or not c:
        raise HTTPException(status_code=404, detail="Student or Course not found")
    # Insert association
    try:
        db.execute(StudentCourse.insert().values(student_id=sid, course_id=course_id))
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Already enrolled")
    return {"ok": True}

@router.get("/students/{sid}/courses")
def list_student_courses(sid: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    from sqlalchemy import select
    stmt = select(Course).join(StudentCourse, Course.id == StudentCourse.c.course_id).where(StudentCourse.c.student_id == sid)
    courses = db.execute(stmt).scalars().all()
    return {"items": courses}
