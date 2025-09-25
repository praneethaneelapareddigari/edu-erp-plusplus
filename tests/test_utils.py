from utils.grade_calculator import calculate_gpa

def test_calculate_gpa():
    grades = [("A", 3), ("B+", 4), ("A+", 3)]
    assert calculate_gpa(grades) > 0
