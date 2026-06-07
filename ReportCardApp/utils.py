from django.db.models import Sum
from .models import Student


def calculate_gpa_and_grade(total_obtained, total_max):

    if not total_max:
        return 0.0, "N/A"

    percentage = (
        total_obtained / total_max
    ) * 100

    gpa = round(
        (percentage / 100) * 4,
        2
    )

    if gpa >= 3.5:
        grade = "A"
    elif gpa >= 3.0:
        grade = "B"
    elif gpa >= 2.5:
        grade = "C"
    elif gpa >= 1.5:
        grade = "D"
    else:
        grade = "F"

    return gpa, grade


def calculate_rank(student):

    students = (
        Student.objects
        .annotate(
            total=Sum(
                "student_marks__marks_obtained"
            )
        )
        .order_by(
            "-total",
            "student_age"
        )
    )

    rank = 1
    last_score = None
    rank_map = {}

    for s in students:

        if s.total != last_score:
            rank_map[s.id] = rank
        else:
            rank_map[s.id] = rank - 1

        last_score = s.total
        rank += 1

    return rank_map.get(student.id)