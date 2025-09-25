from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from ..models.course import Course
from ..models.faculty import Faculty
from ..models.associations import FacultyCourse, StudentCourse
from ..schemas.course import CourseCreate, CourseOut
from ..auth import get_current_user

router = APIRouter()

@router.post("/courses", response_model=CourseOut)
def create_course(payload: CourseCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    c = Course(code=payload.code, name=payload.name, credits=payload.credits, faculty=payload.faculty)
    db.add(c)
    try:
        db.commit()
        db.refresh(c)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate course code")
    return c

@router.get("/courses/{cid}", response_model=CourseOut)
def get_course(cid: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    c = db.get(Course, cid)
    if not c:
        raise HTTPException(status_code=404, detail="Course not found")
    return c

@router.get("/courses")
def list_courses(limit: int = Query(20, ge=1, le=200), offset: int = Query(0, ge=0), q: str | None = None,
                 db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    query = db.query(Course)
    if q:
        like = f"%{q}%"
        query = query.filter((Course.name.ilike(like)) | (Course.code.ilike(like)))
    total = query.count()
    items = query.order_by(Course.id).limit(limit).offset(offset).all()
    return {"total": total, "items": items}

@router.post("/courses/{cid}/assign-faculty/{fid}")
def assign_faculty(cid: int, fid: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    c = db.get(Course, cid)
    f = db.get(Faculty, fid)
    if not c or not f:
        raise HTTPException(status_code=404, detail="Course or Faculty not found")
    try:
        db.execute(FacultyCourse.insert().values(course_id=cid, faculty_id=fid))
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Already assigned")
    return {"ok": True}

@router.get("/courses/{cid}/students")
def list_course_students(cid: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    from ..models.student import Student
    stmt = select(Student).join(StudentCourse, Student.id == StudentCourse.c.student_id).where(StudentCourse.c.course_id == cid)
    students = db.execute(stmt).scalars().all()
    return {"items": students}

@router.get("/courses/{cid}/faculties")
def list_course_faculties(cid: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    stmt = select(Faculty).join(FacultyCourse, Faculty.id == FacultyCourse.c.faculty_id).where(FacultyCourse.c.course_id == cid)
    faculties = db.execute(stmt).scalars().all()
    return {"items": faculties}
