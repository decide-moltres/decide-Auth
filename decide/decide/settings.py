"""
Django settings for decide project.
Generated by 'django-admin startproject' using Django 2.0.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^##ydkswfu0+=ofw0l#$kv^8n)0$i(qd&d&ol#p9!b$8*5%j1+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

from django.utils.translation import ugettext_lazy as _

# Application definition

INSTALLED_APPS = [
	'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'social_django',
    'social_core',
    'corsheaders',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'gateway',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning'
}

AUTHENTICATION_BACKENDS = [
    'base.backends.AuthBackend',


    'social_core.backends.github.GithubOAuth2', # <--
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth', # <--
    'social_core.backends.facebook.FacebookOAuth2', # <--
    'social_core.backends.reddit.RedditOAuth2',
    'social_core.backends.telegram.TelegramAuth',
    'social_core.backends.spotify.SpotifyOAuth2',
    'social_core.backends.pinterest.PinterestOAuth2',
    'social_core.backends.box.BoxOAuth2',
    'social_core.backends.vk.VKOAuth2',

    'django.contrib.auth.backends.ModelBackend', # <--	  
    'authentication.backends.EmailAuthBackend',

]

MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

BASEURL = 'https://decidemoltresauth.herokuapp.com/'

APIS = {
    'authentication': BASEURL,
    'base': BASEURL,
    'booth': BASEURL,
    'census': BASEURL,
    'mixnet': BASEURL,
    'postproc': BASEURL,
    'store': BASEURL,
    'visualizer': BASEURL,
    'voting': BASEURL,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware', # <--

]

ROOT_URLCONF = 'decide.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'authentication/templates') ,
		],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',


                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--
            ],
        },
    },
]

WSGI_APPLICATION = 'decide.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'decide',
        'USER': 'decide',
        'PASSWORD': 'decide',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGES = (
    ('en-us', _('English')),
    ('es-es', _('Español')),

)

LANGUAGE_CODE = 'en-us'
_ = lambda s: s

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

# Versioning
ALLOWED_VERSIONS = ['v1', 'v2']
DEFAULT_VERSION = 'v1'

try:
    from local_settings import *
except ImportError:
    print("local_settings.py not found")

# loading jsonnet config
if os.path.exists("config.jsonnet"):
    import json
    from _jsonnet import evaluate_file
    config = json.loads(evaluate_file("config.jsonnet"))
    for k, v in config.items():
        vars()[k] = v


LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


# Authentication

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '407573137056-c4f14n6t9jkivkvlfuhg9n2fqt01ho7i.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'MzuuGAIRT-CeMzwA0i55KM2s'
SOCIAL_AUTH_GITHUB_KEY = 'e69430a687158c2c9a23'
SOCIAL_AUTH_GITHUB_SECRET = '92831c01913b6bd76f0acf03d41d59dce3f5b7f9'
 
INSTALLED_APPS = INSTALLED_APPS + MODULES
django_heroku.settings(locals())

SOCIAL_AUTH_LOGIN_ERROR_URL = 'home'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'home'
SOCIAL_AUTH_RAISE_EXCEPTIONS = True

SOCIAL_AUTH_FACEBOOK_KEY = '572053296676935'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'b9e748f263a09917bb2c5a6f918aee9b'  # App Secret

SOCIAL_AUTH_REDDIT_KEY = 'kXx1spRf4zz6aw'  # App ID
SOCIAL_AUTH_REDDIT_SECRET = 'YhwOUO8nxCklIuK7Ph3MQVmkNdk'  # App Secret

SOCIAL_AUTH_SPOTIFY_KEY = 'a0e947034c4e466890e56f7b16d42bcf'
SOCIAL_AUTH_SPOTIFY_SECRET = '57899192a5244b2683034e59ac8f02cf'

SOCIAL_AUTH_PINTEREST_KEY = '5076324617361072271'
SOCIAL_AUTH_PINTEREST_SECRET = '7c05409999886a4a788da691ef1cfdb23b452dd03cf4fbc9eee042ef5c685fdd'
SOCIAL_AUTH_PINTEREST_SCOPE = [
    'read_public',
    'write_public',
    'read_relationships',
    'write_relationships'
]

SOCIAL_AUTH_BOX_KEY = 'xfhv6juai5fq19l7soz0mmqucig7a1q0'
SOCIAL_AUTH_BOX_SECRET = 'NJbkDZB31gi8qzRzxLMI8hMNBhWXTDnG'

SOCIAL_AUTH_SPOTIFY_SCOPE = ['user-read-email', 'user-library-read']
SOCIAL_AUTH_VK_OAUTH2_KEY = '7270253'
SOCIAL_AUTH_VK_OAUTH2_SECRET = '674998ac674998ac674998ac63672777c166749674998ac395e96870d4fdde734b972c0'

TELEGRAM_BOT_NAME = 'Decide-Auth'

SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = '833892302:AAFJ6RTuuKmHiscwehvUKfBcZeoYw3gcQA4'
TELEGRAM_BOT_TOKEN = '833892302:AAFJ6RTuuKmHiscwehvUKfBcZeoYw3gcQA4'
TELEGRAM_LOGIN_REDIRECT_URL = ''

