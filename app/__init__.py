from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.openhours.views import openhours_blueprint
app.register_blueprint(openhours_blueprint, url_prefix='/openhours')

from app import views, models
