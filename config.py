from os.path import abspath, dirname, join
import logging

_cwd = dirname(abspath(__file__))

class BaseConfiguration(object):
    SERVER_NAME = 'localhost:8080'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'scorepy.db')
    #SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'scorepy.log'
    LOGGING_LEVEL = logging.INFO

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

class TestingConfiguration(BaseConfiguration):
    Testing = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    HASH_ROUNDS = 1
