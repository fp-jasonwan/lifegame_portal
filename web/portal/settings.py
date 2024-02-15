"""
Django settings for portal project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os 
import environ
from urllib.parse import urlparse
from google.oauth2 import service_account
import platform
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, True))

env_file = os.path.join(BASE_DIR, ".env.prod")

if os.path.isfile(env_file):
    # Use a local secret file, if provided
    env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uj6g7vig$awvjj)4#dugs%)rm5sy%nbhjn2adesox!aynp&5%-'

# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to Cloud Run. This code takes the URL and converts it to both these settings formats.
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    # CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
    # SECURE_SSL_REDIRECT = True
    # SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS.append('lionslifegame.web.app')
ALLOWED_HOSTS.append('lionslifegame.firebaseapp.com')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = [
    'https://*.a.run.app', 
    "https://a.run.app",
    "https://lionslifegame.web.app", 
    "https://lionslifegame.firebaseapp.com",
    "https://www.lionslifegame.web.app", 
    "https://*.lionslifegame.web.app",
    # 'http://127.0.0.1'
    ]
CSRF_COOKIE_DOMAIN = [
    ".web.app", 
    ".firebaseapp.com",
    ".a.run.app"
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'booth',
    'player',
    'account',
    'news',
    'oc',
    'main',
    'django_tables2',
    'constance',
    'constance.backends.database',
    'qr_code',
    "storages",
    'widget_tweaks',
    'django_extensions',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.login.AuthRequiredMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'corsheaders.middleware.CorsPostCsrfMiddleware'
]

ROOT_URLCONF = 'portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portal.wsgi.application'



# Database
if platform.system() == 'Windows':
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lifegame',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '104.154.249.55',
        'PORT': '5432',
    }
    }
else:
    DATABASES = {"default": env.db()}

    # If the flag as been set, configure to use proxy
    if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
        DATABASES["default"]["HOST"] = "cloudsql-proxy"
        DATABASES["default"]["PORT"] = 5432


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'portal.db')
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Hong_Kong'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

GS_BUCKET_NAME = env("GS_BUCKET_NAME")
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"

LOGIN_REDIRECT_URL = '/'
STATIC_URL = "/static/"
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'account.User'


# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
from collections import OrderedDict

CONSTANCE_ADDITIONAL_FIELDS = {
    'game_mode': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (
            ("opening", "Opening"),
            ("start", "Start"),
            ("closing", "Closing")
        )
    }],
    'room': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (
            ("yes", "yes"),
            ("no", "no"),
        )
    }],
}


CONSTANCE_CONFIG = {
    'SITE_NAME': ('青少年人生之旅', 'Website title'),
    'ANNOUNCEMENT': ('', '公告'),
    'HALL_LINK': ('', '禮堂連結'),
    'GAME_MODE': ('opening', 'Select game mode', 'game_mode'),
    'SHARING_LINK': ('', ''),
    'RULES': ('', ''),
    'room': ('', 'room start', 'room'),
}
