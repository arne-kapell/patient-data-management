"""
Django settings for patient_data_management project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from base64 import b64decode, b64encode
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-43&7229&ro7_g(to0494&#is$^g=%i*fxf&0bug3)r6bdroll!")

# SECURITY WARNING: don't run with debug turned on in production!
# use env if available
DEBUG = bool(int(os.getenv("DEBUG", default=0)))

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'cloud.arne-kapell.de']
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://127.0.0.1',
                        'http://0.0.0.0', 'https://cloud.arne-kapell.de']
# CSRF_COOKIE_SECURE = not bool(int(os.getenv("DEBUG", default=0)))

# Application definition

INSTALLED_APPS = [
    "pdm.apps.PdmConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # 'whitenoise.runserver_nostatic',
    "django.contrib.staticfiles",
    "encrypted_files"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "patient_data_management.urls"

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

WSGI_APPLICATION = "patient_data_management.wsgi.application"
# WHITENOISE_USE_FINDERS = True
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "pdm.User"

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
URL_PREFIX = os.getenv("URL_PREFIX", default="")

STATIC_URL = URL_PREFIX + "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

LOGIN_URL = URL_PREFIX + "/accounts/login/"
LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = 'index'
# LOGOUT_REDIRECT_URL = URL_PREFIX + 'index'

SESSION_COOKIE_AGE = 30 * 60  # in seconds (30 minutes)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ACCEPTED_DOCUMENT_EXTENSIONS = [
    "pdf",
    "docx",
    "doc",
    "odt",
    "jpg",
    "jpeg",
    "png"
]
NO_PREVIEW_DOCUMENT_EXTENSIONS = [
    "docx",
    "doc",
    "odt"
]

FILE_UPLOAD_HANDLERS = [
    "encrypted_files.uploadhandler.EncryptedFileUploadHandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
]

AES_KEY = b64decode(os.getenv("DOCUMENT_ENCRYPTION_KEY",
                    default=b64encode(os.urandom(32))))

MAX_PAST_DAYS_FOR_ACCESS_REQUEST = 30 * 6  # 6 months
MAX_FUTURE_DAYS_FOR_ACCESS_REQUEST = 30 * 6  # 6 months

STATES_BY_CODE = {
    "BW": "Baden-Württemberg",
    "BY": "Bayern",
    "BE": "Berlin",
    "BB": "Brandenburg",
    "HB": "Bremen",
    "HH": "Hamburg",
    "HE": "Hessen",
    "MV": "Mecklenburg-Vorpommern",
    "NI": "Niedersachsen",
    "NR": "Nordrhein",
    "NW": "Westfalen-Lippe",
    "RP": "Rheinland-Pfalz",
    "SL": "Saarland",
    "SN": "Sachsen",
    "SA": "Sachsen-Anhalt",
    "SH": "Schleswig-Holstein",
    "TH": "Thüringen"
}
STATE_DOCTOR_INDEX_MAPPING = {
    "BW": "http://www.arztsuche-bw.de/",
    "BY": "http://arztsuche.kvb.de/",
    "BE": "http://www.kvberlin.de/60arztsuche/index.html",
    "BB": "https://www.laekb.de/PublicNavigation/arzt/mitgliedschaft/arztsuche/",
    "HB": "http://www.kvhb.de/arztsuche",
    "HH": "https://www.aerztekammer-hamburg.org/arztsuche.html",
    "HE": "http://arztsuchehessen.de/",
    "MV": "https://www.kvmv.de/service/arztsuche/",
    "NI": "http://www.arztauskunft-niedersachsen.de/",
    "NR": "https://www.aekno.de/presse/arztsuchen",
    "NW": "https://portal.aekwl.de/web/serviceportal/arztsuche#suche",
    "RP": "https://www.praxisfinder-rlp.de/sprechzeit",
    "SL": "https://www.aerztekammer-saarland.de/aerzte/informationenfueraerzte/arztsuche/",
    "SN": "http://www.gesundheitsinfo-sachsen.de/",
    "SA": "https://arztinfo.kvsa.de/ases-kvsa/ases.jsf",
    "SH": "https://arztsuche.kvsh.de/",
    "TH": "http://www.kv-thueringen.de/arztsuche/"
}

VERIFY_REQUEST_COOLDOWN = 60 * 60 * 24  # 24 hours

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'

PASSWORD_RESET_TIMEOUT = 60 * 60 * 24  # 24 hours
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    MAILER_EMAIL_BACKEND = EMAIL_BACKEND
    EMAIL_HOST = os.environ.get("EMAIL_HOST", default="smtp.strato.de")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", default="")
    EMAIL_HOST_USER = os.environ.get(
        "EMAIL_HOST_USER", default="no-reply@cloud.arne-kapell.de")
    EMAIL_PORT = 465
    EMAIL_USE_SSL = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
