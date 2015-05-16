from flask import render_template, json, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask_limiter.util import get_ipaddr
from app.models import User, Trade, db
from app import app, limiter
from .forms import UserForm


@app.route('/')
@app.route('/index')
@limiter.exempt
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("100/day;10/hour")
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
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("100/day;10/hour")
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
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            json_data = request.get_json()
            return "JSON Message: " + str(json_data)
        else:
            return "415 Unsupported Media Type"
    else:
        return render_template('trade.html')
