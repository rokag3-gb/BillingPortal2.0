from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = '!fmxo(%&l(nigi1-ew*90w-tmuv08en90=7###&5((c4@&by9-'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

KICC_EASYPAY = {
    "JS_URL":"http://testpg.easypay.co.kr/webpay/EasypayCard_Web.js",
    "STORE_ID":"T5102001",
    "STORE_NAME":"CLOUDMATE",
    "CHARSET": "UTF-8",
    "CURRENCY": "00", # 00: KRW
    "LANG": "KOR"
}