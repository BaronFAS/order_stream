from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_app.settings import Config

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_app import (constants, gbq, models, order_app, settings, data_processing, validators,)  # noqa
