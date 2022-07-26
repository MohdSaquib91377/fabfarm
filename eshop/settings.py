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
    'jazzmin',
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
    ),
   
    
}

# JWT configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=config('seconds',cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=config('seconds',cast=int)),
  
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



CSRF_TRUSTED_ORIGINS = ['https://fab-farm.datavivservers.in']

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
RAZORPAY_WEBHOOK_KEY_SECRET = config("RAZORPAY_WEBHOOK_KEY_SECRET")

# Elastic Search

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}

# redis configuration
# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'


# Django Jazzmin Package to customized Admin pannel

JAZZMIN_SETTINGS = {
   # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "FabFarm.com",
    # Title on the brand, and login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Venya Admin",
    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "logo/VenyaLogo.png",
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Venya",
    # Copyright on the footer
    "copyright": "venya private limited",
    # Field name on user model that contains avatar image
    "user_avatar": None,
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    # "order_with_respect_to": ["account", "books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
   # "custom_links": {
        #"books": [{
         #   "name": "Make Messages", 
        #    "url": "make_messages", 
       #     "icon": "fas fa-comments",
      #      "permissions": ["books.view_book"]
     #   }]
    #},

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "account.CustomUser": "fas fa-user",
        "auth.Group": "fas fa-users",
        "banner.Banner":"fas fa-border",
        "banner.Page":"fas fa-file",
        "cart.Cart":"fas fa-cart-plus",
        "coupon.Coupon":"fas fa-gift",
        "order.Order":"fab fa-first-order",
        "order.OrderItem":"fab fa-first-order-alt",
        "payment.Payment":"fas fa-dollar-sign",
        "store.Brand":"fa fa-rocket",
        "store.Category":"fas fa-boxes",
        "store.Image":"fas fa-image",
        "store.Product":"fas fa-pizza-slice",
        "store.RecentView":"fas fa-eye",
        "store.SubCategory":"fas fa-boxes",
        "wishlist.Wishlist":"fas fa-heart"


    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
        "default_icon_children": "fas fa-globe-europe",
        #################
        # Related Modal #
        #################
        # Use modals instead of popups
        "related_modal_active": False,
        #############
        # UI Tweaks #
        #############
        # Relative paths to custom CSS/JS scripts (must be present in static files)
        "custom_css": None,
        "custom_js": None,
        # Whether to show the UI customizer on the sidebar
        "show_ui_builder": True,
        ###############
        # Change view #
        ###############
        # Render out the change view as a single form, or in tabs, current options are
        # - single
        # - horizontal_tabs (default)
        # - vertical_tabs
        # - collapsible
        # - carousel
        "changeform_format": "horizontal_tabs",
        # override change forms on a per modeladmin basis
        "changeform_format_overrides": {
            "auth.user": "horizontal_tabs",
            "auth.group": "horizontal_tabs",
        },
        # how many objects show er page
        "list_per_page": config("LIST_PER_PAGE", cast=int, default=20),
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    # "accent": "accent-lime",
    # "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    # "sidebar": "sidebar-dark-primary",
    # "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": True,
    # "theme": "solar",
    # "dark_mode_theme": "darkly",
    # "button_classes": {
    #     "primary": "btn-primary",
    #     "secondary": "btn-secondary",
    #     "info": "btn-outline-info",
    #     "warning": "btn-outline-warning",
    #     "danger": "btn-outline-danger",
    #     "success": "btn-outline-success"
    # },
    "actions_sticky_top": True,
}