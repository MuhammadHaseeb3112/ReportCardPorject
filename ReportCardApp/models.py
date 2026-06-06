from django.db import models


class Department(models.Model):
    department = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.department

    class Meta:
        ordering = ['department']
        verbose_name = 'Department'


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="subjects")

    def __str__(self):
        return self.subject_name

    class Meta:
        ordering = ['subject_name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class Student(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="students")
    student_id = models.CharField(max_length=20, unique=True)   # e.g. STU-1001
    student_name = models.CharField(max_length=100)
    student_age = models.IntegerField(default=18)
    student_email = models.EmailField(unique=True)
    student_address = models.TextField()

    def __str__(self):
        return f"{self.student_name} ({self.student_id})"

    class Meta:
        ordering = ['student_name']
        verbose_name = 'Student'


class SubjectMarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_marks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()

    class Meta:
        unique_together = ('student', 'subject')  # prevent duplicate marks entry
        verbose_name = "Subject Mark"
        verbose_name_plural = "Subject Marks"

    def __str__(self):
        return f"{self.student.student_name} - {self.subject.subject_name}"

    @property
    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100 if self.total_marks > 0 else 0
