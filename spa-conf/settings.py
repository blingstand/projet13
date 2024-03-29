"""
Django settings for spa project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# projets (1), projets/projet13 (2), projets/projet13/spa-conf (3)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT) 
ROOT_DIR = os.path.dirname(BASE_DIR)

# print("1", ROOT_DIR)
# print("2", BASE_DIR)
# print("3", PROJECT_ROOT)

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7691-0!3k#_q=4&l4s*-qs^d42+n8vi5f&6$2vedf*cc4g13fg'

ALLOWED_HOSTS = ["*"]
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mydashboard.apps.MyDashboardConfig',
    'user.apps.UserConfig',
    'spa_core.apps.SPACoreConfig',
    'sheet.apps.SheetConfig',
    'mail.apps.MailConfig', 
    'info.apps.InfoConfig', 
    'search_bar.apps.SearchBarConfig', 
    # "django_nose", 
    "tests.apps.TestsConfig"
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'spa-conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Cette ligne ajoute le dossier templates/ à la racine du projet
            os.path.join(ROOT_DIR, 'user/templates'),
            os.path.join(ROOT_DIR, 'dashboard/templates'),
            os.path.join(ROOT_DIR, 'spa-conf/templates'),
            os.path.join(ROOT_DIR, 'spa_core/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'search_bar.context_processors.search_form'
            ],
        },
    },
]

WSGI_APPLICATION = 'spa-conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'spa', # le nom de notre base de donnees creee precedemment
        'USER': 'bling', # attention : remplacez par votre nom d'utilisateur
        'PASSWORD': '123',
        'HOST': '',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

#for django-nose
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# NOSE_ARGS = [
#     '--with-coverage',
#     '--cover-tests',
#     '--cover-package=sheet, mail, mydashboard',
#     '--cover-html'
# ]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

DATE_FORMAT = '%m/%d/%Y'

STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'spa_core/static'),
    )
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.AppDirectoriesFinder',    #causes verbose duplicate notifications in django 1.9
)

# SHORT_DATE_FORMAT='d/m/Y'