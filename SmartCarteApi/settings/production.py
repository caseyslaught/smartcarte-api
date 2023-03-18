import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from SmartCarteApi.settings.base import *

# AWS

COGNITO_USERPOOL_NAME = "smartcarte-production"
COGNITO_USERPOOL_ID = os.environ['SMARTCARTE_PROD_COGNITO_USERPOOL_ID']
COGNITO_APP_ID = os.environ['SMARTCARTE_PROD_COGNITO_APP_ID']


# Django

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'api.smartcarte.earth',
    'production.eba-kapt8bmu.us-west-2.elasticbeanstalk.com'
]
DEBUG = False
STAGE = 'production'

DATABASE_NAME = "smartcarte"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': os.environ['SMARTCARTE_MYSQL_USER'],
        'PASSWORD': os.environ['SMARTCARTE_MYSQL_PASSWORD'],
        'HOST': os.environ['SMARTCARTE_MYSQL_HOST'],
        'PORT': '3306',
    },
    'OPTIONS': {
        'charset': 'utf8mb4',
        'use_unicode': True,
    }
}

# Sentry

SENTRY_PROJECT_ID = os.environ['SMARTCARTE_SENTRY_PROJECT_ID']

sentry_sdk.init(
    dsn=f"https://b600ddba30304e76ad027d33c43d5ced@o4504860083224576.ingest.sentry.io/{SENTRY_PROJECT_ID}",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.01,
    send_default_pii=False
)

