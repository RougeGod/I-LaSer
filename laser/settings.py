"""Contains the configuration options for the entire site
"""
import os
import logging
from platform import system
import django


DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__)) + '/'

SITE_ROOT = os.path.dirname(os.path.realpath(__file__)) + '/'

#ori APP_ROOT = os.path.join(SITE_ROOT, 'transducer/')  #SK1 tried changing this to:
APP_ROOT = SITE_ROOT      #SK1 added this

#SK1  TEMP_SK = os.path.join(SITE_ROOT, 'transducer/')  #SK1 --> SK added this line
#SK1  CODE_GEN = os.path.join(TEMP_SK, 'code_gen/')    #SK1 --> SK tried use this instead of next
CODE_GEN = os.path.join(APP_ROOT, 'code_gen/')

LIMIT = 500000
LIMIT_AUTOMATON = 250

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
WSGI_APPLICATION = 'laser.wsgi.application'

CACHES = {
    'default':
    {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

if DEBUG:
    # will output to your console
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
    )
else:
    # will output to logging file
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filename='/my_log_file.log',
        filemode='a'
    )

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4tl4s9!yv3nqz8o1t8%f(@=b7_a36swulrn572sg&r*&jl#5^i'

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'laser.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MEDIA_ROOT = '/var/www/project/media/' if system() == 'Linux' \
    else 'C:\\cygwin64\\home\\Matthew\\LaSer\\media'
    # Change this to whateveryou need if developing on Windows
MEDIA_URL = '/media/'


STATIC_ROOT = '/var/www/project/static'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static/"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.staticfiles',
    #'laser.DEV.SK.templates', #SK added this, but then not even the main worked
)

