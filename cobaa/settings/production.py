from .base import *

DEBUG = False

if 'WEBSITE_HOSTNAME' in os.environ:
    ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME'], 'cobaa.library.ohio.gov']
    CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME'], 'https://cobaa.library.ohio.gov']
else:
    ALLOWED_HOSTS = ['cobaa.library.ohio.gov']
    CSRF_TRUSTED_ORIGINS = ['https://cobaa.library.ohio.gov']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/mnt/database/db.sqlite3',
        'OPTIONS': {
            'timeout': 30,
            'transaction_mode': 'IMMEDIATE',
            'init_command': '''
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA cache_size=-64000;
                PRAGMA temp_store=MEMORY;
                PRAGMA mmap_size=268435456;
                PRAGMA optimize;
            '''
        }
    }
}
