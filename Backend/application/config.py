import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quantified_self_database.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY =  "myappquantifie"
    SECURITY_TOKEN_MAX_AGE=3600
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_USERNAME_ENABLE=True
    SECURITY_TOKEN_AUTHENTICATION_HEADER="A-T"
    SECURITY_PASSWORD_SALT='secret'
    WTF_CSRF_ENABLED = False
    CORS_SUPPORTS_CREDENTIALS=True
    CORS_EXPOSE_HEADERS='A-T'
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quantified_self_database.sqlite3'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    # app.config['SECRET_KEY']='myappquantifie'
    #
    # app.config['SECURITY_UNAUTHORIZED_VIEW']= None
    # app.config['SECURITY_USERNAME_ENABLE']=True
    # app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER']="A-T"
    # app.config['SECURITY_TOKEN_MAX_AGE']=3600
    # app.config['SECURITY_PASSWORD_SALT']='secret'
    # app.config['WTF_CSRF_ENABLED'] = False
    # app.config['CORS_SUPPORTS_CREDENTIALS']=True
    # app.config['CORS_EXPOSE_HEADERS']='A-T'
