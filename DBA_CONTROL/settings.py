"""
Django settings for DBA_CONTROL project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import sys
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# print(os.path.join(BASE_DIR, 'DBA_CONTROL\\apps'))  # D:\usage_work\课设\数据库课设\DBA_CONTROL\DBA_CONTROL\apps
sys.path.insert(0, os.path.join(BASE_DIR, 'DBA_CONTROL\\apps'))  # 使app路径被识别为app

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t((w3h1_p*+8$@0kxxukiw=**$4aq8%6on=0)5lnxcutkt0=s-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 允许哪些域名访问Django
ALLOWED_HOSTS = ['127.0.0.1', 'Localhost']
# CORS追加白名单（显然针对的是前端域名）（后端可能自己识别不到自己吗？）
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',   # DRF
    'user.apps.UserConfig',  # 用户模块
    'cmts.apps.CmtsConfig',  # 院校专业老师学生模块
    'classes.apps.ClassConfig',  # 班级教研模块
    'courses.apps.CoursesConfig',  # 学生课程模块

    'corsheaders',          # 解决跨域CORS
    'rest_framework_simplejwt',  # jwt
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',    # 最外层的中间件（先解决跨域问题了再走下面的中间件，所以放最前面）
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DBA_CONTROL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'   # %s为字符串 %d为整数，levelname代表级别（五种：DEBUG/INFO/WARNING/ERROR/CRITICAL），asctime为时间，module打印模块名称，lineno打印日志级别的数值，message为信息
        },
        'simple': {
        	'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
        	'()': 'django.utils.log.RequireDebugTrue',  # Debug为True
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',   # 输出级别
            'filters': ['require_debug_true'],  # 指定上面写的过滤器（过滤添加为Debug为true才能向控制台输出）
            'class': 'logging.StreamHandler',
            'formatter': 'simple'  # 输出格式，也是上面写的格式simple
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/dba_control.log"),  # 日志文件的位置（需要创建目录logs），那么就需要BASE_DIR的dirname即上一级目录
            'maxBytes': 300 * 1024 * 1024,  # 300兆，若超过，则再创建一个，在文件名后加1 2 ...
            'backupCount': 10,              # 若文件超过十个，将会删除
            'formatter': 'verbose',         # 输出格式，也是上面写的格式verbose
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器（后续获取logger对象的时候会使用到）
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    },
}

WSGI_APPLICATION = 'DBA_CONTROL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 配置redis缓存
CACHES = {
    # 默认缓存配置
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_codes": {  # 缓存验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# 发送邮箱配置(注释掉的配置为全局已经有的默认配置)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_PORT = 25
EMAIL_HOST = 'smtp.163.com'   # 邮箱服务器
# 发送邮件的邮箱
EMAIL_HOST_USER = 'lxd2534891955@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'MQFAOXAEQJTEALXO'
# 收件⼈看到的发件⼈
EMAIL_FROM = 'GDUT龙洞助手<lxd2534891955@163.com>'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # jwt配置
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # JWT有效期
}

# 修改默认的认证后端
AUTHENTICATION_BACKENDS = [
 'user.auth.MyAuthBackend',
]

# 配置自定义用户表MyUser
AUTH_USER_MODEL = 'user.User'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 多人开发时，无法共享的本地配置可以放到新建的 local_settings.py 文件中
# 并且把 local_settings.py 加入版本管理忽略文件中
try:
    from local_settings import *  # noqa
except ImportError:
    pass
