import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_app.settings import Config

load_dotenv()

app = Flask(__name__)
app.config['FLASK_APP'] = os.getenv('FLASK_APP')
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')

app.config.from_object(Config)
db = SQLAlchemy(app)


from flask_app import (constants, gbq, models, order_app, settings, data_processing, validators,)  # noqa
