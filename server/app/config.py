import os
from dotenv import load_dotenv  

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom(24)  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


    #MAIL_SERVER = 'smtp.gmail.com'
    #MAIL_PORT = 587
    #MAIL_USE_TLS = True
    #MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    #MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    #MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

    

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    #SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'postgresql://graduate_db_user:simplepassword123@localhost/graduate_db')


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
