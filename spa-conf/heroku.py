from . import *



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["spa-bergerac.herokuapp.com"]

#this is for {load static} ex : {% static "jquery.js" %} => "/static/jquery.js"
STATIC_URL = '/static/'

#location for manage.py collectstatic
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

#In production collectstatic gathers the data in spa-conf/static.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
    
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
    'NAME': 'd11tp1l8afags2', # le nom de notre base de donnees creee precedemment
    'USER': 'apfhedbrevwcts', # attention : remplacez par votre nom d'utilisateur
    'PASSWORD': 'ec125269cad507880d779a48e1072b7a229e670bccfc85f5faa538616583fb2a',
    'HOST': 'ec2-3-210-255-177.compute-1.amazonaws.com',
    'PORT': '5432',
	}
}
