from pathlib import Path,os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# load_dotenv(env_path)

# SECRET_KEY = os.getenv("SECRET_KEY")

SECRET_KEY = 'your-secret-key' 

DEBUG = False

ALLOWED_HOSTS = ['mytechhub.blog']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'techhub.apps.TechhubConfig',
    'accounts.apps.AccountsConfig'
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

ROOT_URLCONF = 'mySite.urls'

WSGI_APPLICATION = 'mySite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'DB_NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("USER"),
        'PASSWORD': os.getenv("PASSWORD"),
        'HOST': os.getenv("HOST"),
        'PORT': os.getenv("DB_PORT", "3306"),
    }
}

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# ✅  設定を追加（Django管理機能のエラーを防ぐ）
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
                'django.template.context_processors.media',
            ],
        },
    },
]


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

AUTHENTICATION_BACKENDS = [
    'accounts.auth_backend.CustomAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# データベースセッションを使用
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage' 


USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'mypage'

LOGOUT_REDIRECT_URL = 'toppage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 開発環境では STATICFILES_DIRS を使用する
if os.getenv("DJANGO_ENV") == "development":
    STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# メディアファイルの保存先を定義
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")