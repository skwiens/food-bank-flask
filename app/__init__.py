#app/__init__

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# import the blueprints
from app.volunteers.views import volunteers_blueprint
from app.users.views import users_blueprint
from app.openhours.views import openhours_blueprint

# register the blueprints
app.register_blueprint(volunteers_blueprint, url_prefix='/volunteers')
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(openhours_blueprint, url_prefix='/openhours')

from app import views, models, forms
