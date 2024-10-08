from .base import *

DEBUG = False

ADMINS = [('David W. Green', 'dgreen@library.ohio.gov',)]

if 'WEBSITE_HOSTNAME' in os.environ:
    ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME'], 'cobaa.library.ohio.gov']
else:
    ALLOWED_HOSTS = ['cobaa.library.ohio.gov']

if 'WEBSITE_HOSTNAME' in os.environ:
    CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME'], 'https://cobaa.library.ohio.gov']
else:
    CSRF_TRUSTED_ORIGINS = ['https://cobaa.library.ohio.gov']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '',
        'OPTIONS': {
            'connect_timeout': 5,
        }
    },
}
