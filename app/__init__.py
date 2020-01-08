from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for
from app.models import db, Users, Expenses
from flask_login import LoginManager, login_required

from app.forms import SignUpForm

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

@login_manager.user_loader()
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
        return
    return render_template('signup.html',form=register_form)

@app.route('/login')
def login():
    return

@app.route('/logout')
@login_required
def logout():
    return