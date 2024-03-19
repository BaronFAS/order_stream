import os


class Config(object):
    # DATA_DIR = '../data' if os.name == 'nt' else '/order_app/flask_app/data'
    DATA_DIR = '../flask_app/data'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DATA_DIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
