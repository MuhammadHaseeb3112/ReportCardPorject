from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F, FloatField
from io import BytesIO
from .models import Student, Department
from django.contrib.auth.decorators import login_required


# --------------------------
# Helpers
# --------------------------
def calculate_gpa_and_grade(total_obtained, total_max):
    """Calculate GPA (out of 4.0) and Grade from marks."""
    if not total_max or total_max == 0:
        return 0.0, "N/A"

    percentage = (total_obtained / total_max) * 100
    gpa = round((percentage / 100) * 4, 2)

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
    """Return the student's rank among all students (optimized with annotate)."""
    students_with_totals = (
        Student.objects.annotate(total=Sum("student_marks__marks_obtained"))
        .order_by("-total", "student_age")
    )

    rank = 1
    last_score = None
    rank_map = {}

    for s in students_with_totals:
        if s.total != last_score:
            rank_map[s.id] = rank
        else:
            rank_map[s.id] = rank - 1  # same score → same rank
        last_score = s.total
        rank += 1

    return rank_map.get(student.id)


# --------------------------
# Static Pages
# --------------------------
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


# --------------------------
# Student List with Filters + Pagination
# --------------------------
def student_list(request):
    students = Student.objects.all()
    departments = Department.objects.all()

    # --- Filters ---
    search_query = request.GET.get("q", "")
    dept_filter = request.GET.get("department", "")

    if search_query:
        students = students.filter(
            Q(student_name__icontains=search_query)
            | Q(student_id__icontains=search_query)
            | Q(student_email__icontains=search_query)
        )

    if dept_filter:
        students = students.filter(department_id=dept_filter)

    # --- Pagination ---
    paginator = Paginator(students, 10)  # 10 students per page
    page_number = request.GET.get("page")
    students_page = paginator.get_page(page_number)

    context = {
        "page_obj": students_page,
        "departments": departments,
        "search_query": search_query,
        "dept_filter": dept_filter,
    }
    return render(request, "students/student_list.html", context)


# --------------------------
# Leaderboard (Top 10 Students)
# --------------------------
@login_required
def leaderboard(request):
    students = (
        Student.objects.annotate(
            total_obtained=Sum("student_marks__marks_obtained", output_field=FloatField()),
            total_max=Sum("student_marks__total_marks", output_field=FloatField()),
        )
        .order_by("-total_obtained")[:10]
    )

    # Attach GPA, Grade, and Rank
    students = list(students)  # so we can enumerate
    for idx, student in enumerate(students, start=1):
        total_obtained = student.total_obtained or 0
        total_max = student.total_max or 0
        gpa, grade = calculate_gpa_and_grade(total_obtained, total_max)

        student.gpa = gpa
        student.grade = grade
        student.rank = idx

    return render(request, "students/leaderboard.html", {"students": students})


# --------------------------
# Student Report (HTML)
# --------------------------
@login_required
def student_report(request, pk):
    student = get_object_or_404(Student, pk=pk)
    marks = student.student_marks.all()

    total_obtained = sum(m.marks_obtained for m in marks)
    total_max = sum(m.total_marks for m in marks)

    gpa, grade = calculate_gpa_and_grade(total_obtained, total_max)
    rank = calculate_rank(student)
    percentage = (total_obtained / total_max) * 100 if total_max > 0 else 0

    context = {
        "student": student,
        "gpa": gpa,
        "grade": grade,
        "percentage": round(percentage, 2),
        "rank": rank,
        "total_max": total_max,  # so we can show "GPA out of 4.0"
    }
    return render(request, "students/student_report.html", context)


# --------------------------
# Student Report (PDF)
# --------------------------
@login_required
def student_report_pdf(request, pk):
    student = get_object_or_404(Student, pk=pk)
    marks = student.student_marks.all()

    total_obtained = sum(m.marks_obtained for m in marks)
    total_max = sum(m.total_marks for m in marks)
    gpa, grade = calculate_gpa_and_grade(total_obtained, total_max)
    rank = calculate_rank(student)

    # --- PDF Build ---
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph(
        "<para align='center'><b><font size=16 color='blue'>Student Report Card</font></b></para>",
        styles["Normal"],
    )
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Student Info
    info_data = [
        ["Name:", student.student_name, "Student ID:", student.student_id],
        ["Department:", student.department.department, "Age:", str(student.student_age)],
        ["Email:", student.student_email, "Address:", student.student_address],
    ]
    info_table = Table(info_data, colWidths=[80, 150, 80, 180])
    info_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Marks Table
    marks_data = [["Subject", "Obtained", "Total", "Percentage"]]
    for mark in marks:
        percentage = (mark.marks_obtained / mark.total_marks) * 100 if mark.total_marks > 0 else 0
        marks_data.append(
            [
                mark.subject.subject_name,
                str(mark.marks_obtained),
                str(mark.total_marks),
                f"{round(percentage, 2)}%",
            ]
        )

    marks_table = Table(marks_data, colWidths=[150, 80, 80, 100])
    marks_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    elements.append(marks_table)
    elements.append(Spacer(1, 20))

    # GPA, Grade, Rank
    summary_para = Paragraph(
        f"<para align='center'><font size=12>"
        f"<b>🎓 GPA:</b> {gpa} / 4.0 &nbsp;&nbsp; "
        f"<b>📊 Grade:</b> {grade} &nbsp;&nbsp; "
        f"<b>🏅 Rank:</b> {rank}"
        f"</font></para>",
        styles["Normal"],
    )
    elements.append(summary_para)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{student.student_id}_report.pdf"'
    response.write(pdf)
    return response
