import os
from os import environ

from openwebpos.utils import gen_urlsafe_token

SECRET_KEY = gen_urlsafe_token(16)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# database
DB_DIALECT = 'sqlite'
DB_DRIVER = 'mysqldb'
DB_USER = environ.get('DB_USER')
DB_PASS = environ.get('DB_PASS')
DB_HOST = environ.get('DB_HOST')
DB_PORT = environ.get('DB_PORT')
DB_NAME = environ.get('DB_NAME')

if DB_DIALECT == 'sqlite':
    db_uri = 'sqlite:///' + os.path.join(os.getcwd(), 'openwebpos.db')
else:
    db_uri = f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
