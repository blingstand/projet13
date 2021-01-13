from . import *

print("cpanel prod")


# SECURITY WARNING: keep the sd3gf51qecret key used in production secret!
SECRET_KEY = '#91@b+@ __è-jfuevgtykofnui168431q35g13r)6%i9v+i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["adrienclupot.com"]

STATIC_URL = '/static/'

STATIC_ROOT = '/home/adridwbs/public_html/static'

#In production collectstatic gathers the data in spa-conf/static.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#db_from_env = dj_database_url.config(conn_max_age=600)
#DATABASES['default'].update(db_from_env)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'adridwbs_spa',
        'USER': 'adridwbs', 
        'PASSWORD': 'SStorngol2',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
