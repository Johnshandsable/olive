import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '0d9daedf53df7e7a6cdf042b0f3c0731'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
