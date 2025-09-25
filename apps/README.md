# Frappe Integration (Optional Advanced)

This repo ships with DocType JSON stubs for ERP-like modules. To use Frappe UI:

## Quick Bench Steps
1. Install bench & setup a site (see Frappe docs).
2. Create a custom app, then copy the DocType JSON folders from `apps/` into your app.
3. Run `bench --site yoursite migrate` and create records via Desk.
4. (Optional) Expose REST via Frappe's APIs or keep FastAPI as your external-facing API.

## Files
- `student/doctype/student/student.json`
- `course/doctype/course/course.json`
- `faculty/doctype/faculty/faculty.json`
- `exam/doctype/exam/exam.json`
