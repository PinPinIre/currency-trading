import os

DEBUG = True
SECRET_KEY = os.environ['CF_SECRET_KEY']
SQLALCHEMY_DATABASE_URI = os.environ['CF_DATABASE_URI']
BCRYPT_LOG_ROUNDS = 15
CSRF_ENABLED = True
RATELIMIT_STORAGE_URL = os.environ['CF_REDIS_DATABASE_URI']
