import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """
    mysql> create database microblog character set utf8 collate utf8_bin;
    mysql> create user 'microblog'@'localhost' identified by '<db-password>';
    mysql> grant all privileges on microblog.* to 'microblog'@'localhost';
    mysql> flush privileges;
    mysql> quit;
    """
