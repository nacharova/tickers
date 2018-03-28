# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


#  основные настройки
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'Bah6yee8Mievee6sAhVoh6AiUogh3eiheeGhi2au'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SUBJECT_PREFIX = os.getenv('FLASKY_MAIL_SUBJECT_PREFIX') or "none"
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_TO = os.environ.get('MAIL_TO')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = '25'
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    BABEL_DEFAULT_LOCALE = 'ru'
    BABEL_DEFAULT_TIMEZONE = 'Asia/Yekaterinburg'
    YEAR_OF_BIRTH = 2017
    ITEMS_PER_PAGE = 8
    PREFIX_NAME = os.getenv('PREFIX_NAME') or 'tickers_'
    CSRF_ENABLED = True

    DEFAULT_FOLDER = os.path.join(os.path.dirname(__file__), 'default')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app/static/data/')
    UPLOAD_FOLDER_IMAGE = os.path.join(os.path.dirname(__file__), 'app/static/uploads/')
    FONTS_FOLDER = os.path.join(os.path.dirname(__file__), 'app/static/fonts/')
    THUMBNAIL_FOLDER = os.path.join(os.path.dirname(__file__), 'app/static/data/thumbnail/')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    try:
        os.mkdir(UPLOAD_FOLDER)
        os.mkdir(UPLOAD_FOLDER_IMAGE)
    except OSError:
        pass

    @staticmethod
    def init_app(app):
        pass


#  настройки для разработки
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.sqlite'


#  настройки для тестирования
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../data-test.sqlite')


#  настройка для работы
class ProductionConfig(Config):
    DEBUG = False
    base_user = os.environ.get('BASE_USER') or ''
    base_name = os.environ.get('BASE_NAME') or ''
    base_passwd = os.environ.get('BASE_PASSWORD') or ''
    base_host = os.environ.get('BASE_HOST') or 'localhost'
    if base_passwd:
        SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s'.format() % (base_user, base_passwd, base_host, base_name)
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///data-dev.sqlite'


#  варианты настроек, используються в __init__.py при вызове create_app из manage.py
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
