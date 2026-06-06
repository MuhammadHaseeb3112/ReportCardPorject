# 🎓 Report Card Management System

A Django-based Student Report Card Management System that helps manage student academic records, rankings, departments, and performance analytics. The system provides secure authentication, report card generation, student leaderboards, and performance tracking through a modern web interface.

---

# 🚀 Features

## Authentication System

* User Registration
* User Login & Logout
* Password Reset via Email
* Password Change Functionality
* Secure Authentication System

## Student Management

* Student Records Management
* Department-wise Student Organization
* Student Performance Tracking
* Academic Report Generation
* Individual Student Profiles

## Report Card System

* Generate Student Report Cards
* Subject-wise Marks Management
* Grade Calculation
* Percentage Calculation
* Academic Performance Analysis

## Leaderboard System

* Student Ranking
* Top Performers Dashboard
* Department-wise Ranking
* Merit List Generation
* Performance Comparison

## Dashboard

* Student Overview
* Academic Statistics
* Performance Insights
* Ranking Analytics

## Security Features

* Authentication Protected Views
* Login Required Access
* Secure Form Validation
* CSRF Protection
* User Session Management

---

# 🛠️ Tech Stack

## Backend

* Python
* Django 5

## Frontend

* HTML5
* CSS3
* Bootstrap
* Django Templates

## Database

* SQLite

## Authentication

* Django Authentication System

## Email Services

* SMTP Email Integration
* Password Reset Emails

---

# 📂 Project Structure

```text
ReportCardPorject/
│
├── ReportCardApp/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   │   ├── students/
│   │   ├── home.html
│   │   ├── about.html
│   │
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── fake_data.py
│
├── accounts/
│   ├── templates/
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── password_reset.html
│   │
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── ReportCardPorject/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
└── requirements.txt
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/MuhammadHaseeb3112/ReportCardPorject.git
cd ReportCardPorject
```

## Create Virtual Environment

```bash
python -m venv env
```

## Activate Virtual Environment

### Windows

```bash
env\Scripts\activate
```

### Linux / macOS

```bash
source env/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## Apply Migrations

```bash
python manage.py migrate
```

## Create Superuser

```bash
python manage.py createsuperuser
```

## Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

---

# 📸 Screenshots

Add screenshots of:

* Home Page
* Student List
* Student Report Card
* Leaderboard
* Login Page
* Signup Page
* Password Reset Page

---

# 🎯 Learning Outcomes

This project demonstrates:

* Django Models
* Authentication & Authorization
* CRUD Operations
* Django Forms
* Database Relationships
* Ranking Algorithms
* Leaderboard Systems
* Email Integration
* Session Management
* Template Inheritance
* Secure Web Development

---

# 🔮 Future Improvements

* Django REST Framework API
* JWT Authentication
* Redis Caching
* Celery Background Tasks
* PDF Report Card Generation
* Export Reports to Excel
* Advanced Search & Filtering
* Student Attendance System
* Teacher Dashboard
* Parent Portal
* Notifications System
* PostgreSQL Integration
* Docker Deployment

---

# 👨‍💻 Author

Muhammad Haseeb

GitHub:
https://github.com/MuhammadHaseeb3112

---

# ⭐ Support

If you found this project useful, consider giving it a star on GitHub.
