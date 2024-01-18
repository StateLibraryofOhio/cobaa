from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['STAGE_DB_NAME'],
        'USER': os.environ['STAGE_DB_USER'],
        'PASSWORD': os.environ['STAGE_DB_PASS'],
        'HOST': os.environ['STAGE_DB_HOST'],
        'PORT': '',
        },
    }
