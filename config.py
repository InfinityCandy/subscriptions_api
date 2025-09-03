from decouple import config as de_config


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///subscriptions.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = de_config('SECRET_KEY')
