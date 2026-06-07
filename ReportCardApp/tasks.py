from celery import shared_task

from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

from .models import Student
from .pdf_utils import generate_student_pdf
from .utils import (
    calculate_gpa_and_grade,
    calculate_rank,
)


@shared_task(
    bind=True,
    max_retries=3
)
def send_report_email(
    self,
    student_id
):
    try:

        student = Student.objects.get(
            id=student_id
        )

        # Prevent duplicate emails
        if student.result_published:
            return (
            f"Already published for "
            f"{student.student_email}"
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
            "generated_on": timezone.now(),
        }

        pdf_bytes = generate_student_pdf(
            context
        )

        email = EmailMessage(
            subject="🎓 Student Report Card",
            body=f"""
Hello {student.student_name},

Your academic report card is attached.

Regards,
MH Report System
""",
            from_email=settings.EMAIL_HOST_USER,
            to=[
                student.student_email
            ],
        )

        email.attach(
            f"{student.student_id}_report.pdf",
            pdf_bytes,
            "application/pdf",
        )

        email.send(
            fail_silently=False
        )

        # Mark as published ONLY after successful email
        student.result_published = True

        student.email_sent_at = (
            timezone.now()
        )

        student.save(
            update_fields=[
                "result_published",
                "email_sent_at",
            ]
        )

        return (
            f"Report sent to "
            f"{student.student_email}"
        )

    except Student.DoesNotExist:

        return (
            f"Student with ID "
            f"{student_id} not found."
        )

    except Exception as exc:

        if self.request.retries >= self.max_retries:
            return (
            f"Failed permanently: "
            f"{student.student_email}"
        )

        raise self.retry(
            exc=exc,
            countdown=120,
        )