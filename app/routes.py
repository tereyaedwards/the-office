from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Characters
from werkzeug.urls import url_parse
import requests



@app.route('/')
@app.route('/index')
@login_required
def index():
        return render_template('index2.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # if username is true and check_password comes back true
        # then log user in and take them to next page
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
        # otherwise let them know their info is invalid and return to login page
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/Tereya', methods=['GET', 'POST'])
def Tereya():

    charid = '7'
    url = "https://the-office.p.rapidapi.com/{}".format(charid)

    headers = {
        'x-rapidapi-host': "the-office.p.rapidapi.com",
        'x-rapidapi-key': "666103d036msh1131169c5b9c02bp13d3ecjsna3964c136807"
    }

    response = requests.request("GET", url, headers=headers)
    resp_json = response.json()

    id = resp_json['id']
    name = resp_json['name']
    realname= resp_json['realname']
    seasons= resp_json['seasons']

# if name does not exist add to table
    name_exists = db.session.query(db.exists().where(Characters.name == name)).scalar()
    if not name_exists:
        char_input = Characters(id=id, name=name, realname=realname, seasons=seasons)
        db.session.add(char_input)
        db.session.commit()

    return render_template('Tereya.html', title='Tereya')


@app.route('/MichaelScott')
def MichaelScott():
    return render_template('MichaelScott.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Creates a record that will be inserted(added/committed) into the DB
        # instead of using the "set_password" function I just left it as plain text inside or DB
        user = User(username=form.username.data, email=form.email.data)# password=form.password.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
