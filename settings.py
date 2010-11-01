# Django settings for transitlabour project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'transitlabour_django'
DATABASE_USER = 'andycat'
DATABASE_PASSWORD = 'andycat!!'
DATABASE_HOST = 'mysql.transitlabour.asia'
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Sydney'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/andycat_/transitlabour.asia/transitlabour/templates/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/custom/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jdhd&kno0!c9+ywj1)2*a0g%^&cg_-!x)0cz_^&p02@r%u!te-'

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

ROOT_URLCONF = 'transitlabour.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/andycat_/transitlabour.asia/transitlabour/templates',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.syndication',
    'transitlabour.transitlabourapp',
    'tinymce',
    'registration',
    'profiles',
    'solango',
    'filebrowser',
)

ACCOUNT_ACTIVATION_DAYS = 7

TINYMCE_JS_URL = '/custom/js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = '/home/andycat_/transitlabour.asia/transitlabour/templates/media/js/tiny_mce/'
TINYMCE_DEFAULT_CONFIG = {'theme': "advanced", 'relative_urls': False, 'plugins': "table,paste,searchreplace,media", 'theme_advanced_buttons3_add' : "search,replace, paste, table, media", "extended_valid_elements" : "audio[src|controls]", }
TINYMCE_COMPRESSOR = False
TINYMCE_FILEBROWSER = True

FILEBROWSER_URL_TINYMCE = '/custom/js/tiny_mce/'
FILEBROWSER_PATH_TINYMCE = TINYMCE_JS_ROOT

FILEBROWSER_URL_FILEBROWSER_MEDIA = "/custom/filebrowser/"

LOGIN_URL = "/admin/"
LOGIN_REDIRECT_URL = "http://transitlabour.asia/"

DEFAULT_FROM_EMAIL='info@transitlabour.asia'
AUTH_PROFILE_MODULE = "transitlabourapp.UserProfile"

