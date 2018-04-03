# -*- coding: utf-8 -*-
import os


#  основные настройки
class Config:

    @staticmethod
    def init_app(app):
        pass


#  настройки для разработки
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://tickers:tickers@192.168.0.71/postgres'


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
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://tickers:tickers@192.168.0.71/postgres'


#  варианты настроек, используются в __init__.py при вызове create_app из manage.py
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
