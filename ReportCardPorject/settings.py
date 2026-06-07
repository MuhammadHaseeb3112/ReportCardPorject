from pathlib import Path
from dotenv import load_dotenv
import os

# --------------------------------------------------

# BASE DIRECTORY

# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------

# SECURITY

# --------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
"127.0.0.1",
"localhost",
"10.179.96.217",
]

# --------------------------------------------------

# APPLICATIONS

# --------------------------------------------------

INSTALLED_APPS = [
"django.contrib.admin",
"django.contrib.auth",
"django.contrib.contenttypes",
"django.contrib.sessions",
"django.contrib.messages",
"django.contrib.staticfiles",

"widget_tweaks",

"accounts",
"ReportCardApp",

]

# --------------------------------------------------

# MIDDLEWARE

# --------------------------------------------------

MIDDLEWARE = [
"django.middleware.security.SecurityMiddleware",
"django.contrib.sessions.middleware.SessionMiddleware",
"django.middleware.common.CommonMiddleware",
"django.middleware.csrf.CsrfViewMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
"django.contrib.messages.middleware.MessageMiddleware",
"django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------

# URLS

# --------------------------------------------------

ROOT_URLCONF = "ReportCardPorject.urls"

# --------------------------------------------------

# TEMPLATES

# --------------------------------------------------

TEMPLATES = [
{
"BACKEND": "django.template.backends.django.DjangoTemplates",
"DIRS": [],
"APP_DIRS": True,
"OPTIONS": {
"context_processors": [
"django.template.context_processors.request",
"django.contrib.auth.context_processors.auth",
"django.contrib.messages.context_processors.messages",
],
},
},
]

# --------------------------------------------------

# WSGI

# --------------------------------------------------

WSGI_APPLICATION = "ReportCardPorject.wsgi.application"

# --------------------------------------------------

# DATABASE (POSTGRESQL)

# --------------------------------------------------

DATABASES = {
"default": {
"ENGINE": "django.db.backends.postgresql",
"NAME": os.getenv("DB_NAME"),
"USER": os.getenv("DB_USER"),
"PASSWORD": os.getenv("DB_PASSWORD"),
"HOST": os.getenv("DB_HOST", "localhost"),
"PORT": os.getenv("DB_PORT", "5432"),
}
}

# --------------------------------------------------

# PASSWORD VALIDATION

# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
{
"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
},
{
"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
},
{
"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
},
{
"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
},
]

# --------------------------------------------------

# INTERNATIONALIZATION

# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# --------------------------------------------------

# STATIC FILES

# --------------------------------------------------

STATIC_URL = "static/"

STATICFILES_DIRS = [
BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# --------------------------------------------------

# AUTH REDIRECTS

# --------------------------------------------------

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "login"

# --------------------------------------------------

# EMAIL SETTINGS

# --------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST")

EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --------------------------------------------------

# CELERY

# --------------------------------------------------

CELERY_BROKER_URL = os.getenv(
    "REDIS_URL"
)

CELERY_RESULT_BACKEND = os.getenv(
    "REDIS_URL"
)

# --------------------------------------------------

# DEFAULT PK

# --------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
