from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from ..db import Base

StudentCourse = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
    UniqueConstraint("student_id", "course_id", name="uq_student_course")
)

FacultyCourse = Table(
    "faculty_courses",
    Base.metadata,
    Column("faculty_id", Integer, ForeignKey("faculties.id", ondelete="CASCADE"), nullable=False),
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
    UniqueConstraint("faculty_id", "course_id", name="uq_faculty_course")
)
