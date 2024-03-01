from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_app.settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from flask_app import order_app, constants, settings, models, gbq  # noqa
