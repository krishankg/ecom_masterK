




import os
import django_heroku
from decouple import config
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3mc3x@*nju()3uiys(7&-w*g8zys(mg4jjx-=49ien+jt=fz&4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products.apps.ProductsConfig',
    'crispy_forms',
    'tag',
    'carts',
    'user',
    'orders',
    'billing',
    'addresses',
    'user_info',
    'naomi',
    'django_inlinecss',
    'payments',
    'stripe',
]

AUTH_USER_MODEL='user.UserModel'
LOGIN_URL='users:login'
LOGIN_REDIRECT_URL='/'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
BASE_URL='http://127.0.0.1:8000'


FORCE_SESSION_TO_ONE= False
FORCE_INACTIVE_USER_ENDSESSION= False


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# DATABASES = {}
# DATABASES['default'] = dj_database_url.config(conn_max_age=600)



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
DEFAULT_EMAIL_HOST='no-reply@easydealindia.com'
EMAIL_USE_TLS = True
DEFAULT_ACTIVATION_DAYS=1
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# LOGIN_REDIRECT_URL='products:list'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'

STATICFILES_DIRS=[
   os.path.join(BASE_DIR,'ecommerce/static'),
]

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'ecommerce/media')




CELERY_BROKER_URL='redis://localhost'
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_TASK_SERIALIZER='json'


STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

django_heroku.settings(locals())
