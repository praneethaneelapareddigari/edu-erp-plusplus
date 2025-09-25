import csv
from collections import defaultdict

def generate_timetable(csv_path: str) -> dict:
    """CSV columns: student_roll, day, time, course_code"""
    result = defaultdict(list)
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result[row['student_roll']].append({
                'day': row['day'],
                'time': row['time'],
                'course': row['course_code']
            })
    return dict(result)
