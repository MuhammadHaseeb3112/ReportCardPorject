import csv
from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from .models import Department, Subject, Student, SubjectMarks


# ---------------- Department ----------------
class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("department",)
    search_fields = ("department",)
    ordering = ("department",)


# ---------------- Subject ----------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("subject_name", "department")
    list_filter = ("department",)
    search_fields = ("subject_name",)
    ordering = ("subject_name",)


# ---------------- Custom Actions ----------------
def calculate_gpa(modeladmin, request, queryset):
    results = []
    for student in queryset:
        marks = SubjectMarks.objects.filter(student=student)
        if marks.exists():
            percentages = [m.percentage for m in marks]
            gpa = round(sum(percentages) / len(percentages) / 20, 2)  # GPA out of 5.0
            results.append(f"{student.student_name} ({student.student_id}) → GPA: {gpa}")
        else:
            results.append(f"{student.student_name} ({student.student_id}) → No Marks Found")

    modeladmin.message_user(request, "\n".join(results))


calculate_gpa.short_description = "📊 Calculate GPA for selected students"


def export_students_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="students_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Student ID", "Name", "Department", "Subject", "Marks Obtained", "Total Marks", "Percentage"])

    for student in queryset:
        marks = SubjectMarks.objects.filter(student=student)
        for m in marks:
            writer.writerow([
                student.student_id,
                student.student_name,
                student.department.department,
                m.subject.subject_name,
                m.marks_obtained,
                m.total_marks,
                round(m.percentage, 2),
            ])

    return response


export_students_csv.short_description = "📥 Export selected students report to CSV"


def export_students_pdf(modeladmin, request, queryset):
    """Generate PDF report cards for selected students"""
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="students_report_cards.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - inch

    for student in queryset:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, f"Report Card - {student.student_name} ({student.student_id})")
        y -= 20
        p.setFont("Helvetica", 12)
        p.drawString(100, y, f"Department: {student.department.department}")
        y -= 20
        p.drawString(100, y, f"Email: {student.student_email}")
        y -= 20
        p.drawString(100, y, f"Age: {student.student_age}")
        y -= 30

        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Subjects and Marks:")
        y -= 20

        marks = SubjectMarks.objects.filter(student=student)
        if marks.exists():
            total_percentage = 0
            for m in marks:
                p.setFont("Helvetica", 11)
                line = f"{m.subject.subject_name} → {m.marks_obtained}/{m.total_marks} ({round(m.percentage, 2)}%)"
                p.drawString(120, y, line)
                y -= 18
                total_percentage += m.percentage

            gpa = round(total_percentage / len(marks) / 20, 2)  # GPA out of 5
            y -= 10
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, y, f"GPA: {gpa}")
            y -= 30
        else:
            p.setFont("Helvetica", 11)
            p.drawString(120, y, "No marks available.")
            y -= 30

        # New page for next student
        p.showPage()
        y = height - inch

    p.save()
    return response


export_students_pdf.short_description = "📄 Export selected students report to PDF"


# ---------------- Student ----------------
class SubjectMarksInline(admin.TabularInline):
    model = SubjectMarks
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "student_name", "department", "student_email", "student_age")
    list_filter = ("department",)
    search_fields = ("student_name", "student_id", "student_email")
    ordering = ("student_name",)
    inlines = [SubjectMarksInline]
    actions = [calculate_gpa, export_students_csv, export_students_pdf]


# ---------------- Subject Marks ----------------
@admin.register(SubjectMarks)
class SubjectMarksAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "marks_obtained", "total_marks", "percentage")
    list_filter = ("subject", "student__department")
    search_fields = ("student__student_name", "subject__subject_name")
    ordering = ("student", "subject")
