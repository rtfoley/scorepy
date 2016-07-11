from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))

SERVER_NAME = 'localhost:8080'
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'scorepy.db')
#SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
