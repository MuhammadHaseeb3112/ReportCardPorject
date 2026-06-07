from io import BytesIO

from django.template.loader import render_to_string

from weasyprint import HTML


def generate_student_pdf(context):

    html = render_to_string(
        "students/pdf_report.html",
        context
    )

    pdf_file = BytesIO()

    HTML(
        string=html
    ).write_pdf(
        target=pdf_file
    )

    pdf = pdf_file.getvalue()

    pdf_file.close()

    return pdf