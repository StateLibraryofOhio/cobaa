from .base import *

DEBUG = False

ADMINS = [('David W. Green', 'dgreen@library.ohio.gov',)]

ALLOWED_HOSTS = ['cobaa.library.ohio.gov', '127.0.0.1', 'localhost']

CSRF_TRUSTED_ORIGINS = ['https://cobaa.library.ohio.gov', 'http://127.0.0.1', 'http://localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '',
        },
    }
