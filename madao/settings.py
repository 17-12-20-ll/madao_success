import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'd-q62%x@k$150a%lsbe1)(x12k7p)@1gvghs80fp_y)kn63l5a'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'common',
    'tweet'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'madao.urls'
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
WSGI_APPLICATION = 'madao.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库类型
        'NAME': 'madao',  # 数据库名
        'HOST': 'localhost',  # 120.79.47.68 数据库主机号
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '1107',
        'TIME_ZONE': 'Asia/Chongqing',  # 时区要和程序中的时区统一
    }
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
# --------------------- 使用django-redis --------------配置登录token ------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:ll1107@127.0.0.1:6379/1",  # "redis://:密码@127.0.0.1:6379/0"
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# 验证码过期时间 五分钟过期时间（包含手机验证码、图形验证码）
CODE_TIME_OUT = 5 * 60
# 测试验证码过期时间 三个小时
CODE_TIME_OUT_TEST = 3 * 60 * 60
# 登录的token过期时间 一周的过期时间
LOGIN_TIME_OUT = 7 * 24 * 60 * 60
# 管理员登录token过期时间
LOGIN_ADMIN_TIME_OUT = 24 * 60 * 60

# --------------------------- 极光短信的KEY、密钥
APP_KEY = '6759726e4464795d16049679'
MASTER_SECRET = '6fc889d095608ab2b847ced8'
