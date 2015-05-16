from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from app import app
from . import bcrypt

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, index=True, unique=True)
    _password = db.Column(db.String)
    trades = db.relationship('Trade', backref='issuer', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    currencyFrom = db.Column(db.String)
    currencyTo = db.Column(db.String)
    amountSell = db.Column(db.Float)
    amountBuy = db.Column(db.Float)
    rate = db.Column(db.Float)
    timePlaced = db.Column(db.DateTime)
    originatingCountry = db.Column(db.String)

    def __init__(self, user, cfrom, cto, sell, buy, rate, time, origin):
        self.tradeId = db.Column(db.Integer, primary_key=True)
        self.userId = user
        self.currencyFrom = cfrom
        self.currencyTo = cto
        self.amountSell = sell
        self.amountBuy = buy
        self.rate = rate
        self.timePlaced = time
        self.originatingCountry = origin
