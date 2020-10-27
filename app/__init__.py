from flask import Flask, session
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.debug = True
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# doesn't allow you to go to the next page unless you login
login.login_view = 'login'

bootstrap = Bootstrap(app)

from app import routes, models


