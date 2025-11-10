from .base import *

# Detect environment
IS_AZURE = 'WEBSITE_HOSTNAME' in os.environ
DEBUG = not IS_AZURE  # Debug on for local, off for Azure

# Host configuration
if IS_AZURE:
    ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME'], 'cobaa.library.ohio.gov']
    CSRF_TRUSTED_ORIGINS = [
        'https://' + os.environ['WEBSITE_HOSTNAME'],
        'https://cobaa.library.ohio.gov'
    ]
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'http://localhost']

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUDINARY_CLOUD_NAME'],
    'API_KEY': os.environ['CLOUDINARY_API_KEY'],
    'API_SECRET': os.environ['CLOUDINARY_API_SECRET'],
}

# Database configuration
if IS_AZURE:
    db_name = '/mnt/database/db.sqlite3'
else:
    db_name = BASE_DIR / 'db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': db_name,
        'OPTIONS': {
            'timeout': 30,
            'init_command': '''
                PRAGMA journal_mode=DELETE;
                PRAGMA synchronous=NORMAL;
                PRAGMA cache_size=-64000;
                PRAGMA temp_store=MEMORY;
                PRAGMA mmap_size=268435456;
                PRAGMA optimize;
            '''
        }
    }
}
