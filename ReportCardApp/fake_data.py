from faker import Faker
import random
from .models import Department, Subject, Student, SubjectMarks

fake = Faker()

def generate_fake_data(num_departments=5, students_per_dept=10, subjects_per_dept=5) -> None:
    """
    Generate fake Departments, Subjects, Students, and SubjectMarks.
    """

    try:
        for _ in range(num_departments):
            dept = Department.objects.create(
                department=f"{fake.word().capitalize()} Department"
            )

            # Create Subjects
            subjects = [
                Subject.objects.create(
                    subject_name=fake.word().capitalize(),
                    department=dept
                )
                for _ in range(subjects_per_dept)
            ]

            # Create Students
            for _ in range(students_per_dept):
                student_id = f"STU-{fake.unique.random_int(1000, 9999)}"
                student = Student.objects.create(
                    department=dept,
                    student_id=student_id,
                    student_name=fake.name(),
                    student_age=random.randint(18, 30),
                    student_email=fake.unique.email(),   # 👈 generates real unique emails
                    student_address=fake.address()
                )

                # Assign Marks
                for subj in subjects:
                    total = 100
                    obtained = random.randint(30, 100)
                    SubjectMarks.objects.create(
                        student=student,
                        subject=subj,
                        marks_obtained=obtained,
                        total_marks=total
                    )

        print("✅ Fake data generated successfully!")

    except Exception as e:
        print(f"❌ Error generating fake data: {e}")
