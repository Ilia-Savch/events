from pathlib import Path
from datetime import timedelta
import os
import environ

root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(env.str(root(), ".env"))

SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.str("ALLOWED_HOSTS", default="").split(" ")

BASE_DIR = root()

#################################
# ALL INSTALLED APPS
#################################
# base
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# packages
INSTALLED_APPS += [
    "rest_framework",
    "django_filters",
    "corsheaders",
    "djoser",
    "debug_toolbar",
]

# apps
INSTALLED_APPS += [
    "users",
    "common",
    "api",
    "events",
]

# drf_spectacular after apps
INSTALLED_APPS += [
    "drf_spectacular",
]


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("PG_DATABASE", "postgres"),
        "USER": env.str("PG_USER", "postgres"),
        "PASSWORD": env.str("PG_PASSWORD", "postgres"),
        "HOST": env.str("DB_HOST", "localhost"),
        "PORT": env.str("DB_PORT", 5432),

    },
    "extra": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    },
}

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ("users.models.backends.AuthBackends",)


#################################
# REST FRAMEWORK
#################################
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    # "DEFAULT_PAGINATION_CLASS": "common.pagination.BasePagination",
    # документация
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

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


#################################
# LOCALIZATION
#################################
LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


#################################
# STATIC AND MEDIA
#################################
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#################################
# CORS HEADERS
#################################
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
CSRF_COOKIE_SECURE = False


#################################
# DRF SPECTACULAR
#################################
SPECTACULAR_SETTINGS = {
    "TITLE": "Events",
    "DESCRIPTION": "Platform for events",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "SERVE_AUTHENTICATION": [
        "rest_framework.authentication.BasicAuthentication",
    ],
    "SWAGGER_UI_SETTINGS": {
        "DeepLinking": True,
        "DisplayOperationId": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": False,
}

#################################
# DJOSER
#################################

DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {},
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=7),
}

INTERNAL_IPS = [
    "127.0.0.1",
]

#################################
# REDIS
#################################
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        # change port to redis://redis:6379 and terminate Redis process
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "db": "1",
        },
    }
}

#################################
# CELERY
#################################

# временная зона
CELERY_TIMEZONE = TIME_ZONE

# # к какому redis обращаться
# REDIS_HOST = env.str('REDIS_HOST', default='redis')
# REDIS_PORT = env.str('REDIS_PORT', default=6379)

# # брокер сообщений и бэкэнд результатов
# CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# что использовать в качестве сериализатора, для передачи данных,
# дял бэкэнда результатов
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# если в задаче произошла ошибка, пробрасывать эту ошибку на верх или нет
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# максимальное время исполнения задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

# указываем какой модуль:класс использовать для шедуллера(периодические задачи)
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

#################################
# E-mail smpt configuration
#################################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
