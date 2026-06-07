# 🎓 Report Card Management System

A modern Django-based Student Report Card Management System designed to manage student records, academic performance, report card generation, rankings, and automated result publishing.

The system provides secure authentication, PDF report card generation, asynchronous email delivery using Celery & Redis, leaderboard analytics, and department-wise student management.

---

# 🚀 Key Features

## 🔐 Authentication & Security

* User Registration
* User Login & Logout
* Password Reset via Email
* Password Change Functionality
* Authentication Protected Views
* CSRF Protection
* Secure Session Management
* Staff-only Result Publishing

---

## 👨‍🎓 Student Management

* Student Record Management
* Department-wise Organization
* Student Profiles
* Email Management
* Academic Performance Tracking
* Search & Filtering System
* Pagination Support

---

## 📚 Subject & Marks Management

* Subject-wise Marks Entry
* Department-specific Subjects
* Percentage Calculation
* GPA Calculation
* Grade Calculation
* Rank Calculation
* Performance Analytics

---

## 📄 Professional Report Cards

* Dynamic Report Card Generation
* GPA & Grade Summary
* Rank Information
* Percentage Statistics
* Downloadable PDF Reports
* Professionally Styled PDF Layout
* Generated Timestamp

---

## 🏆 Leaderboard System

* Top Student Rankings
* GPA-based Leaderboard
* Academic Merit Lists
* Performance Comparison
* Top 10 Students Dashboard

---

## 📧 Automated Result Publishing

### Publish Results with One Click

Staff users can:

* Publish all student results
* Automatically generate PDFs
* Email report cards to students
* Prevent duplicate email delivery
* Track email delivery timestamps

### Smart Email Workflow

* Celery Background Tasks
* Redis Message Broker
* Automatic Retry on Failure
* Duplicate Email Prevention
* Delivery Tracking
* Bulk Result Publishing

---

## ⚡ Asynchronous Processing

Powered by Celery and Redis:

* Background Email Sending
* Queue Management
* Retry Mechanism
* Scalable Task Processing
* Non-blocking User Experience

---

# 🛠️ Tech Stack

## Backend

* Python 3
* Django 5
* Celery

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* Django Templates

## Database

* SQLite

## Background Processing

* Celery
* Redis

## PDF Generation

* WeasyPrint

## Email Services

* SMTP
* Gmail App Password Integration

## Authentication

* Django Authentication System

---

# 📂 Project Structure

```
ReportCardPorject/
│
├── ReportCardApp/
│   ├── migrations/
│   ├── templates/
│   │   └── students/
│   ├── models.py
│   ├── views.py
│   ├── tasks.py
│   ├── utils.py
│   ├── pdf_utils.py
│   └── urls.py
│
├── accounts/
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── ReportCardPorject/
│   ├── settings.py
│   ├── celery.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
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

## Activate Environment

### Windows

```bash
env\Scripts\activate
```

### Linux/macOS

```bash
source env/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

EMAIL_HOST_USER=[your_email@gmail.com](mailto:your_email@gmail.com)
EMAIL_HOST_PASSWORD=your_app_password

REDIS_URL=redis://localhost:6379/1
```

---

# 🚀 Run Redis

```bash
redis-server
```

---

# 🚀 Run Celery Worker

```bash
celery -A ReportCardPorject worker -l info
```

---

# 🗄️ Apply Migrations

```bash
python manage.py migrate
```

---

# 👤 Create Superuser

```bash
python manage.py createsuperuser
```

---

# ▶️ Run Development Server

```bash
python manage.py runserver
```

Application:

```
http://127.0.0.1:8000/
```

Admin:

```
http://127.0.0.1:8000/admin/
```

---

# 📸 Screenshots

Include screenshots of:

* Home Page
* Student Dashboard
* Student List
* Student Report Card
* PDF Report Card
* Leaderboard
* Login Page
* Admin Panel
* Result Publishing System

---

# 🎯 What This Project Demonstrates

* Django Models & ORM
* Authentication & Authorization
* CRUD Operations
* Pagination
* Search & Filtering
* GPA Algorithms
* Ranking Algorithms
* PDF Generation
* Celery Task Queues
* Redis Integration
* Email Automation
* Background Processing
* Secure Web Development
* Production-ready Architecture

---

# 🔮 Future Improvements

* Django REST Framework API
* JWT Authentication
* PostgreSQL
* Docker Deployment
* Nginx
* Redis Caching
* Celery Beat Scheduling
* Excel Export
* Teacher Dashboard
* Parent Portal
* Attendance Management
* Kafka Integration
* Microservices Architecture
* FastAPI Notification Service

---

# 👨‍💻 Author

**Muhammad Haseeb**

GitHub:
https://github.com/MuhammadHaseeb3112

---

# ⭐ Support

If you found this project useful, please consider giving it a star ⭐ on GitHub.
