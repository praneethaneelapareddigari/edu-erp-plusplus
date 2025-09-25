from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.faculty import Faculty
from ..schemas.faculty import FacultyCreate, FacultyOut
from ..auth import get_current_user

router = APIRouter()

@router.post("/faculties", response_model=FacultyOut)
def create_faculty(payload: FacultyCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    f = Faculty(name=payload.name, dept=payload.dept, email=payload.email)
    db.add(f)
    try:
        db.commit()
        db.refresh(f)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate email")
    return f

@router.get("/faculties/{fid}", response_model=FacultyOut)
def get_faculty(fid: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    f = db.get(Faculty, fid)
    if not f:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return f

@router.get("/faculties")
def list_faculties(limit: int = Query(20, ge=1, le=200), offset: int = Query(0, ge=0), q: str | None = None,
                   db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    query = db.query(Faculty)
    if q:
        like = f"%{q}%"
        query = query.filter((Faculty.name.ilike(like)) | (Faculty.dept.ilike(like)) | (Faculty.email.ilike(like)))
    total = query.count()
    items = query.order_by(Faculty.id).limit(limit).offset(offset).all()
    return {"total": total, "items": items}
