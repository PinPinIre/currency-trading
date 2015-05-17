from datetime import datetime
from flask_json_multidict import get_json_multidict
from flask import render_template, json, request, redirect, url_for, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask_limiter.util import get_ipaddr
from app.models import User, Trade, db
from app import app, limiter
from .forms import UserForm, TradeForm


@app.route('/')
@app.route('/index')
@limiter.exempt
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
@limiter.exempt
def login():
    # If GET -> serve Login Template
    # Elif POST -> validate form, login user, redirect to /trade
    if current_user.is_authenticated():
        return redirect(url_for('trade'))
    form = UserForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first_or_404()
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect(url_for('trade'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
@login_required
@limiter.exempt
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@limiter.exempt
def register():
    # If GET -> serve Register Template
    # Elif POST -> validate form, try create user, login user, redirect to /trade
    if current_user.is_authenticated():
        return redirect(url_for('trade'))
    form = UserForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User(form.username.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('trade'))
        else:
            return redirect(url_for('register'))
    else:
        return render_template('register.html', form=form)


@app.route('/trade', methods=['GET', 'POST'])
@login_required
@limiter.limit("200/day;20/hour", key_func=lambda: current_user.get_id() if current_user.is_authenticated() else get_ipaddr())
def trade():
    form = TradeForm(request.form)
    if request.method == 'POST':
        json_data = get_json_multidict(request)
        # Ignore CRSF as it was not in the spec, ideally should be true
        form = TradeForm(json_data, csrf_enabled=False)
        if form.validate():
            user = current_user
            time = datetime.strptime(json_data['timePlaced'], '%d-%b-%y %H:%M:%S')
            trade = Trade(json_data['userId'], json_data['currencyFrom'], json_data['currencyTo'], json_data['amountSell'], json_data['amountBuy'], json_data['rate'], time, json_data['originatingCountry'])
            db.session.add(trade)
            db.session.commit()
            return "Trade %s was a success." % trade
        else:
            abort(415)
    else:
        trades = Trade.query.all()
        return render_template('trade.html', form=form, trades=trades)
