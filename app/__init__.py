from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from app import views
from .models import User


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).first()
