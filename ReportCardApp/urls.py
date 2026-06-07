from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("students/", views.student_list, name="student_list"),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path("students/<int:pk>/report/", views.student_report, name="student_report"),
    path("students/<int:pk>/report/pdf/", views.student_report_pdf, name="student_report_pdf"),
    path(
    "publish-results/",
    views.publish_results,
    name="publish_results"
),
]
