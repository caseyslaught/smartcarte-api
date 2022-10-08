from SmartCarteApi.settings.base import *

# AWS

COGNITO_USERPOOL_NAME = "smartcarte-production"
COGNITO_USERPOOL_ID = "" #os.environ['SMARTCARTE_PROD_COGNITO_USERPOOL_ID']
COGNITO_APP_ID = "" #os.environ['SMARTCARTE_PROD_COGNITO_APP_ID']


# Django

ALLOWED_HOSTS = [
    'api.smartcarte.earth',
    'something.eleasticbeanstalk.com'
]
DEBUG = False
STAGE = 'production'

DATABASE_NAME = "smartcarte"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': os.environ['LOCAL_MYSQL_USER'],
        'PASSWORD': os.environ['LOCAL_MYSQL_PASSWORD'],
        'HOST': os.environ['LOCAL_MYSQL_HOST'],
        'PORT': '3306',
    },
    'OPTIONS': {
        'charset': 'utf8mb4',
        'use_unicode': True,
    }
}

