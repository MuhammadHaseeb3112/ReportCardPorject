from .utils import (
    calculate_gpa_and_grade,
    calculate_rank,
)

from .pdf_utils import generate_student_pdf

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.core.paginator import Paginator
from django.db.models import Q, Sum, FloatField
from .models import Student, Department
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib import messages
from django.shortcuts import redirect

from ReportCardApp.tasks import send_report_email
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST






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


@login_required
def student_report_pdf(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    marks = student.student_marks.all()

    total_obtained = sum(
        mark.marks_obtained
        for mark in marks
    )

    total_max = sum(
        mark.total_marks
        for mark in marks
    )

    percentage = (
        (total_obtained / total_max) * 100
        if total_max > 0
        else 0
    )

    gpa, grade = calculate_gpa_and_grade(
        total_obtained,
        total_max
    )

    rank = calculate_rank(
        student
    )

    context = {
        "student": student,
        "marks": marks,
        "gpa": gpa,
        "grade": grade,
        "percentage": round(
            percentage,
            2
        ),
        "rank": rank,
        "total_obtained": total_obtained,
        "total_max": total_max,
            # Add this
         "generated_on": timezone.now(),
    }

    pdf_bytes = generate_student_pdf(
    context
)

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{student.student_id}_report.pdf"'
    )

    response.write(
        pdf_bytes
    )

    return response



@staff_member_required
@require_POST
def publish_results(request):

    students = Student.objects.filter(
        result_published=False
    ).exclude(
        student_email=""
    )

    count = students.count()

    for student in students:

        send_report_email.delay(
            student.id
        )


    messages.success(
    request,
    f"{count} report emails queued successfully."
)

    return redirect(
        "leaderboard"
    )

    
@require_POST    
@staff_member_required
def reset_publish(request):

    updated = Student.objects.update(
    result_published=False,
    email_sent_at=None
)

    messages.success(
    request,
    f"{updated} publish statuses reset."
)
    return redirect(
        "leaderboard"
    )