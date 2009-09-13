import os.path
import sys
import platform
 
PROJECT_ROOT = os.path.dirname(__file__)

DEVELOPMENT_MODE = (platform.node() != "li43-156")
 
if DEVELOPMENT_MODE:
    DEBUG = True
    MEDIA_URL = '/m/'
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = 'dev.db'
    CACHE_BACKEND = 'dummy:///'
else:
    DEBUG = False
    MEDIA_URL = 'http://static.alfakryl.dk/'
    ADMIN_MEDIA_PREFIX = MEDIA_URL + '/admin/'
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_USER = 'alfakryl'
    DATABASE_NAME = 'alfakryl_db'
    
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Johan Bichel Lindegaard', 'mr.bichel@gmail.com'),)
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Copenhagen'
LANGUAGE_CODE = 'dk-DK'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'alfakryl.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'registration',
    'tagging',
    'alfakryl.ink',
)

#EMAIL_HOST = 
#EMAIL_PORT =

ACCOUNT_ACTIVATION_DAYS = 4

try:
    from settings_local import *
except ImportError:
    import sys
    sys.stderr.write('Unable to read settings_local.py\n')
    sys.exit(1)
