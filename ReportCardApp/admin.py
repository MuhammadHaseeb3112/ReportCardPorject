import csv
import zipfile
from io import BytesIO

from django.contrib import admin
from django.http import HttpResponse

from .models import (
    Department,
    Subject,
    Student,
    SubjectMarks,
)

from .tasks import send_report_email
from .pdf_utils import generate_student_pdf


# ==================================================
# Department
# ==================================================

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("department",)
    search_fields = ("department",)
    ordering = ("department",)


# ==================================================
# Subject
# ==================================================

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "subject_name",
        "department",
    )

    list_filter = (
        "department",
    )

    search_fields = (
        "subject_name",
    )

    ordering = (
        "subject_name",
    )


# ==================================================
# Admin Actions
# ==================================================

def calculate_gpa(modeladmin, request, queryset):

    messages = []

    for student in queryset:

        marks = student.student_marks.all()

        if not marks.exists():
            messages.append(
                f"{student.student_name} -> No Marks Found"
            )
            continue

        total_obtained = sum(
            mark.marks_obtained
            for mark in marks
        )

        total_max = sum(
            mark.total_marks
            for mark in marks
        )

        percentage = (
            total_obtained / total_max
        ) * 100

        gpa = round(
            (percentage / 100) * 4,
            2
        )

        messages.append(
            f"{student.student_name} ({student.student_id}) -> GPA: {gpa}"
        )

    modeladmin.message_user(
        request,
        " | ".join(messages)
    )


calculate_gpa.short_description = (
    "📊 Calculate GPA"
)


# ==================================================
# CSV Export
# ==================================================

def export_students_csv(modeladmin, request, queryset):

    response = HttpResponse(
        content_type="text/csv"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="students_report.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Student ID",
        "Student Name",
        "Department",
        "Subject",
        "Obtained",
        "Total",
        "Percentage",
    ])

    for student in queryset:

        marks = student.student_marks.all()

        for mark in marks:

            writer.writerow([
                student.student_id,
                student.student_name,
                student.department.department,
                mark.subject.subject_name,
                mark.marks_obtained,
                mark.total_marks,
                round(mark.percentage, 2),
            ])

    return response


export_students_csv.short_description = (
    "📥 Export Students CSV"
)


# ==================================================
# PDF Export (ZIP)
# ==================================================

def export_students_pdf(modeladmin, request, queryset):

    zip_buffer = BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as zip_file:

        for student in queryset:

            pdf_bytes = generate_student_pdf(
                student
            )

            zip_file.writestr(
                f"{student.student_id}_report.pdf",
                pdf_bytes,
            )

    response = HttpResponse(
        zip_buffer.getvalue(),
        content_type="application/zip",
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="student_reports.zip"'

    return response


export_students_pdf.short_description = (
    "📄 Export Report Cards PDF"
)


# ==================================================
# Email Report Cards
# ==================================================

def send_report_via_email(
    modeladmin,
    request,
    queryset
):

    total = 0

    for student in queryset:

        send_report_email.delay(
            student.id
        )

        total += 1

    modeladmin.message_user(
        request,
        f"{total} report emails queued successfully."
    )


send_report_via_email.short_description = (
    "📧 Send Report Card Email"
)


# ==================================================
# Student
# ==================================================

class SubjectMarksInline(admin.TabularInline):
    model = SubjectMarks
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "student_id",
        "student_name",
        "department",
        "student_email",
        "student_age",
        "result_published",
    )

    list_filter = (
        "department",
    )

    search_fields = (
        "student_name",
        "student_id",
        "student_email",
    )

    ordering = (
        "student_name",
    )

    inlines = [
        SubjectMarksInline
    ]

    actions = [
        calculate_gpa,
        export_students_csv,
        export_students_pdf,
        send_report_via_email,
    ]


# ==================================================
# Subject Marks
# ==================================================

@admin.register(SubjectMarks)
class SubjectMarksAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "subject",
        "marks_obtained",
        "total_marks",
        "percentage",
    )

    list_filter = (
        "subject",
        "student__department",
    )

    search_fields = (
        "student__student_name",
        "subject__subject_name",
    )

    ordering = (
        "student",
        "subject",
    )

    