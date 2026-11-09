#import os to read the secret key from an environment variable if one is set
import os


class Config:
    #secret key used by Flask to protect the forms and the login session
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'music-discovery-dev-key'

    #database settings (replace YOUR_PASSWORD_HERE with your own PostgreSQL password)
    DB_NAME = 'music_discovery'
    DB_USER = 'postgres'
    DB_PASSWORD = 'YOUR_PASSWORD_HERE'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
