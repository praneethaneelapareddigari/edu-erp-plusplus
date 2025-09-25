import csv

def bulk_import_students(csv_path: str) -> list[dict]:
    """CSV columns: name, roll_no, email"""
    students = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({'name': row['name'], 'roll_no': row['roll_no'], 'email': row['email']})
    return students

def bulk_import_courses(csv_path: str) -> list[dict]:
    """CSV columns: code, name, credits, faculty"""
    courses = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            courses.append({
                'code': row['code'],
                'name': row['name'],
                'credits': int(row['credits']),
                'faculty': row.get('faculty') or None
            })
    return courses
