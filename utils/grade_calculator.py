def grade_to_points(grade: str) -> float:
    mapping = {"A+": 10, "A": 9, "B+": 8, "B": 7, "C": 6, "D": 5, "F": 0}
    return mapping.get(grade.upper(), 0)

def calculate_gpa(grades_with_credits: list[tuple[str, int]]) -> float:
    # grades_with_credits: [(grade, credits), ...]
    total_points = 0.0
    total_credits = 0
    for grade, credits in grades_with_credits:
        total_points += grade_to_points(grade) * credits
        total_credits += credits
    return round(total_points / total_credits, 2) if total_credits else 0.0
