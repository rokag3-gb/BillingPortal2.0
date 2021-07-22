from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = [os.getenv('WEBSITE_HOSTNAME',''), '127.0.0.1'] + os.getenv('CUSTOM_DOMAIN','').split(" ")

SECRET_KEY =  os.getenv('SECRET_KEY','')

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv("DB_NAME"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT", '10063'),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'OPTIONS': {
            'driver': os.getenv("DB_DRIVER"),
        },
    }
}

BASE_URL = f'{os.getenv("BASEURL_PROTOCOL","https")}://{APP_HOST}'