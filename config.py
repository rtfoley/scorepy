from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'scorepy.db')
SQLALCHEMY_ECHO = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
