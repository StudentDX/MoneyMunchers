from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for, flash
from app.models import db, Users, Expenses
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from app.forms import SignUpForm, LogInForm

app = Flask(__name__)

app.config['SECRET_KEY'] = urandom(64)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''
login_manager.login_message = 'Log in to view this page!'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    register_form = SignUpForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        password = register_form.password.data
        if Users.query.filter_by(username=username).first() is not None:
            flash('Username is taken!','danger')
        else:
            account = Users(username,password)
            db.session.add(account)
            db.session.commit()
            flash('Account created successfully!','success')
        return redirect(url_for('login'))
    elif request.method == 'POST':
        flash('Account creation failed!','danger')
    return render_template('signup.html',form=register_form)

@app.route('/login',methods=['GET','POST'])
def login():
    login_form = LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = Users.query.filter_by(username=username).first()
        if user is None or user.password != password:
            flash('Incorrect credentials!','danger')
        else:
            login_user(user)
            flash('Logged in successfully!','success')
            return redirect(url_for('home'))
    elif request.method == 'POST':
        flash('Authentication failed!','danger')
    return render_template('login.html',form=login_form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash('Logged out succesfully!','success')
    return redirect(url_for('home'))