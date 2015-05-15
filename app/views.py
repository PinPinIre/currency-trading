from flask import render_template, json, request
from app import app
# TODO: Add rate limit decorator


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If GET -> serve Login Template
    # Elif POST -> validate form, login user, redirect to /trade
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # If GET -> serve Register Template
    # Elif POST -> validate form, try create user, login user, redirect to /trade
    return render_template('register.html')


@app.route('/trade', methods=['GET', 'POST'])
def trade():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            json_data = request.get_json()
            return "JSON Message: " + str(json_data)
        else:
            return "415 Unsupported Media Type"
    else:
        return render_template('trade.html')
