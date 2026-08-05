# ==============================================================================
# IMPORTS
# ==============================================================================

import os
from pathlib import Path

import dj_database_url
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from webpersonal import config_check as cfg

# ==============================================================================
# BASE & ENVIRONMENT SETUP
# ==============================================================================

# Cargo variables de entorno desde el archivo .env
load_dotenv()

# Asigno la ruta del directorio base del proyecto a la variable BASE_DIR
# __file__ es una variable que contiene la ruta del archivo actual settings.py
# .resolve() obtiene la ruta absoluta del archivo actual
# .parent sube un nivel (es como hacer cd..)
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# ENVIRONMENT VALIDATION & VARIABLES
# Validaciones de Variables de Entorno y carga de las mismas.
# ==============================================================================

BUILD = cfg.es_build()

if BUILD == 'True':
    # 2. Valores temporales/dummy para que el build no rompa por variables faltantes
    SECRET_KEY = 'dummy-secret-key-for-build'
    DEBUG = False
    ALLOWED_HOSTS = ['localhost']
    SECRET_KEY = 'dummy-secret-key-for-build'
    DB_SCHEMA = 'dummy'
    DB_URL = 'postgres://dummy:dummy@localhost:5432/dummy'
    SUPABASE_SECRET = 'dummy-supabase-secret'
    SUPABASE_ACCESS_KEY = 'dummy-access-key'
    SUPABASE_PROJECT_ID = 'dummy-project-id'
else:
    GOOGLE_APPLICATION_CREDENTIALS = cfg.validar_google_aplication_credentials()
    DEBUG = cfg.validar_debug()
    ALLOWED_HOSTS = cfg.validar_allowed_hosts()
    SECRET_KEY = cfg.validar_secret_key()
    DB_SCHEMA = cfg.validar_schema()
    DB_URL = cfg.validar_db_url()
    SUPABASE_SECRET = cfg.validar_supabase_secret()
    SUPABASE_ACCESS_KEY = cfg.validar_supabase_access_key()
    SUPABASE_PROJECT_ID = cfg.validar_supabase_project_id()




# ==============================================================================
# CORE CONFIGURATION
# ==============================================================================

ROOT_URLCONF = "webpersonal.urls"
WSGI_APPLICATION = "webpersonal.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==============================================================================
# APPLICATIONS & MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    # Modeltranslation
    "modeltranslation",
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps

    "storages",
    # Local apps
    "core.apps.CoreConfig",
    "cv.apps.CvConfig",
    "portfolio.apps.PortfolioConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware', # habilita /en, /es, /fr, /it
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==============================================================================
# TEMPLATES
# ==============================================================================

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

# ==============================================================================
# DATABASE
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# ==============================================================================

# Creo diccionario DATABASES usando la libreria dj_database_url para parsear
# la URL de la base de datos desde la variable de entorno 'DB_URL'
DATABASES = {
    "default": dj_database_url.config(
        default=DB_URL,
        conn_max_age=600,
        ssl_require=False,  # Esto es lo que activa el cifrado
    )
}

# Le agregamos la opción de PostgreSQL directamente al diccionario resultante:
DATABASES["default"]["OPTIONS"] = {"options": f"-c search_path={DB_SCHEMA}"}


# ==============================================================================
# VALIDACIÓN DE CONTRASEÑAS (Password Validation)
# Reglas de seguridad activas al crear o modificar claves
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        # Evita contraseñas parecidas al nombre de usuario o email
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        # Exige una longitud mínima (8 caracteres)
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        # Evita contraseñas comunes (ej: "123456", "password")
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        # Evita contraseñas puramente numéricas
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]


# ==============================================================================
# INTERNATIONALIZATION (i18n) & LOCALIZATION (l10n)
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# ==============================================================================

# Lista de idiomas soportados por la aplicación para su traducción
LANGUAGES = (
    ("en", _("English")),
    ("pt-br", _("Portuguese")),
    ("it", _("Italian")),
    ("fr", _("French")),
    ("es", _("Spanish")),
)

# Idioma y variante regional por defecto del sitio (Español de Argentina)
LANGUAGE_CODE = "es-AR"
# Habilita el sistema de traducción de mensajes y textos de Django (i18n)
USE_I18N = True
# Habilita el formato automático de fechas, horas y números según la región
USE_L10N = True
# Habilita el soporte para zonas horarias
# (guarda las fechas en UTC en la Base de Datos)
USE_TZ = True
# Zona horaria por defecto para la presentación en los templates
TIME_ZONE = "America/Argentina/Buenos_Aires"

# Agrego carpeta de localización
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# A dónde redirigir después de cambiar idioma si no se especifica una página
REDIRECT_FIELD_NAME = 'next'

# ==============================================================================
# STATIC & MEDIA FILES (Whitenoise + Supabase Storage S3)
# ==============================================================================

# Archivos estáticos
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Le digo a Django que use el backend de S3 de AWS,
# que es compatible con Supabase Storage, para almacenar archivos multimedia.
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Agrego Static General
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Configuro archivos multimedia subidos por usuarios/admin (Supabase Storage)
AWS_ACCESS_KEY_ID = SUPABASE_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = SUPABASE_SECRET
AWS_STORAGE_BUCKET_NAME = "media"

AWS_S3_ENDPOINT_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/storage/v1/s3"

AWS_S3_REGION_NAME = "sa-east-1"
AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_SIGNATURE_VERSION = "s3v4"
# Genera URLs limpias de firmas temporales para buckets públicos
AWS_QUERYSTRING_AUTH = False

AWS_S3_CUSTOM_DOMAIN = (
    f"{SUPABASE_PROJECT_ID}.supabase.co/storage/v1/object/public/"
    f"{AWS_STORAGE_BUCKET_NAME}"
)

# Asigno Media
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

# ==============================================================================
# TEST RUNNER CONFIGURATION
# Configuración del ejecutor de pruebas con esquema aislado
# ==============================================================================

TEST_RUNNER = "webpersonal.test_runner.PostgresSchemaTestRunner"
