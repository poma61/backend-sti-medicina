import dj_database_url
from pathlib import Path
import os
import environ
from datetime import timedelta
from csp.constants import SELF

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

# Hosts del backend
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.0.92",
    "www.core-intern-ai-medicina-upea.site",
    "core-intern-ai-medicina-upea.site",
]

DJANGO_APPS = [
    "django.contrib.auth",  # Vuelve a agregar esta línea
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    # Agregar apps
    "rest_framework",
    # => Para CORS (Cross-Origin Resource Sharing) permitir que el frontend haga solicitudes al backend alojado en otro dominio.
    "corsheaders",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_seeding",
    "csp",
]

PROJECT_APPS = [
    # Aplicaciones del proyecto
    "apps.usuario",
    "apps.estudiante",
    "apps.authentication",
    "apps.personal_institucional",
    "apps.tutor_ai",
    "apps.internado_rotatorio",
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # corsheaders
    "corsheaders.middleware.CorsMiddleware",
    # corsheaders Debe estar antes de CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # "django.middleware.clickjacking.XFrameOptionsMiddleware", # bloquea  FRAME, para visualizar archivos pd
    # others middleware
    "csp.middleware.CSPMiddleware",
]

# Hosts del frontend
# Los llamados autorizados
#CORS_ALLOWED_ORIGINS = [
 # "http://localhost:3000",
 #]
CORS_ALLOW_ALL_ORIGINS = True  # permite todo
CORS_ALLOW_CREDENTIALS = True  # permite todo

# CSRF_COOKIE_DOMAIN = 'http://localhost:8080'

# CSRF_TRUSTED_ORIGINS = [
#   "http://localhost:3000",
# ]
CSRF_TRUSTED_ALL_ORIGINS = True  # permite todo

# Para permitir el contenido
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

CORS_ALLOW_METHODS = (
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
)

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    },
    'other': dj_database_url.config(
        default='postgresql://postgres:postgres@localhost:5432/db_sti_medicina',
        conn_max_age=600
    ),
}

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


# Internationalization
LANGUAGE_CODE = "es"

TIME_ZONE = "America/La_Paz"

USE_I18N = True
USE_L10N = True  # Averiguar que significa
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    # Los usuarios que esten autenticados tendran permisos a las clases
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.authentication.jwt_authentication.CustomJWTAuthentication",
    ),
}


# Permisos de los archivos, para no tener error al subirlos
FILE_UPLOAD_PERMISSIONS = 0o640

# Verificamos si lo quitamos o dejamos
AUTH_USER_MODEL = "usuario.Usuario"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=240),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env("SECRET_KEY"),
}


X_FRAME_OPTIONS = 'SAMEORIGIN'

CONTENT_SECURITY_POLICY = {
    "EXCLUDE_URL_PREFIXES": ("/media*", ),
    "DIRECTIVES": {
        "default-src": [SELF,],
        "script-src": [SELF,],
        "img-src": [SELF,],
        "frame-ancestors": [SELF, "http://localhost:3000", "https://www.intern-ai-medicina-upea.site"],
    },
}
