from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, DecimalField, DateTimeField, PasswordField
from wtforms.validators import Required


class UserForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])


class TradeForm(Form):
    userId = IntegerField('userId', validators=[Required()])
    currencyFrom = TextField('currencyFrom', validators=[Required()])
    currencyTo = TextField('currencyTo', validators=[Required()])
    amountSell = DecimalField('amountSell', validators=[Required()])
    amountBuy = DecimalField('amountBuy', validators=[Required()])
    rate = DecimalField('rate', validators=[Required()])
    timePlaced = DateTimeField('timePlaced', format='%d-%b-%y %H:%M:%S', validators=[Required()])
    originatingCountry = TextField('originatingCountry', validators=[Required()])
