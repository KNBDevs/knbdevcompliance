# config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '*aaaeeeiiiooouuu*'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LANGUAGES = ['es', 'en', 'fr', 'de', 'it', 'pt', 'zh', 'ar', 'hi', 'ru']
    BABEL_DEFAULT_LOCALE = 'es'
    BABEL_DEFAULT_TIMEZONE = 'Europe/Madrid'
