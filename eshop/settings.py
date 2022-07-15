from datetime import timedelta
from corsheaders.defaults import default_headers
from pathlib import Path
import os
from decouple import config,Csv

# from django.views import View
#from .base import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
#BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
#SECRET_KEY = os.environ['SECRET_KEY'] 
#EMAIL_HOST_USER = os.environ.get('profession2291@gmail.com')
#EMAIL_HOST_PASSWORD = os.environ.get()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',default=True)

ALLOWED_HOSTS = config('ALLOWED_HOSTS',default=True,cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'account',
    'store',
    'cart',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders', 
    'order',
    'coupon',
    'wishlist',
    'rest_framework_simplejwt.token_blacklist',
    'payment',
    'banner',
    'django_elasticsearch_dsl', # new
    'search.apps.SearchConfig', # new
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'eshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'eshop.wsgi.application'

# JWT
REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}

# JWT configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('minutes',cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('days',cast=int)),
  
}

# OTP configuration
OTP = {
    "OTP_EXPIRATION_TIME": timedelta(
        minutes=config('minutes',cast=int),
        seconds=config('seconds',cast=int),
    ),
}

#swagger authentication
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,

   'SECURITY_DEFINITIONS': {

      'api_key': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
        'ENGINE': config('DEV_ENGINE'),
        'NAME': config('DEV_NAME'),
        'USER': config('DEV_USER'),
        'PASSWORD': config('DEV_PASSWORD'),
        'HOST': config('DEV_HOST'),
        'PORT': config('DEV_PORT'),
    }
    }

else:
    DATABASES = {
    'default': {
    'ENGINE': config('PROD_ENGINE'),
    'NAME': config('PROD_NAME'),
    'USER': config('PROD_USER'),
    'PASSWORD': config('PROD_PASSWORD'),
    'HOST': config('PROD_HOST'),
    'PORT': config('PROD_PORT'),
    }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_URL = '/static/'

# Base url to serve media files
MEDIA_URL = '/media/'
# Path where media is stored

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000","http://135.181.204.238:8002"
]


CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
)
CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = 'account.CustomUser'


# Email configuration
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Twilio configuration
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')

# Rayzorpay configuration
RAZOR_KEY_ID = config('RAZOR_KEY_ID')
RAZOR_KEY_SECRET = config('RAZOR_KEY_SECRET')

# Elastic Search

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}