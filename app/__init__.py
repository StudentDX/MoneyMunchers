from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for, flash
from app.models import db, Users, Expenses
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from functools import wraps

from app.forms import SignUpForm, LogInForm, BudgetForm, ExpenseForm

app = Flask(__name__)

app.config['SECRET_KEY'] = urandom(64)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''
login_manager.login_message_category = 'danger'
login_manager.login_view = 'login'

def restrict_authenticated(route):
    @wraps(route)
    def restrict(*args,**kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in!','danger')
            return redirect(url_for('profile'))
        return route(*args,**kwargs)
    return restrict

def to_money(decimal):
        return '$'+str(decimal) + ('0' if str(decimal)[-2:] == '.0' else '')

app.jinja_env.filters['to_money'] = to_money

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup',methods=['GET','POST'])
@restrict_authenticated
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
@restrict_authenticated
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
            return redirect(url_for('profile'))
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

@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    if current_user.daily_balance() < 10 and current_user.daily_balance() > 0:
        flash('You are close to exceeding your daily budget.', 'warning')
    if current_user.daily_balance() < 0:
        flash('You have exceeded your daily budget.', 'danger')
    if current_user.monthly_balance() < 10 and current_user.monthly_balance() > 0:
        flash('You are close to exceeding your monthly budget.', 'warning')
    if current_user.monthly_balance() < 0:
        flash('You have exceeded your monthly budget.', 'danger')
    daily_form = BudgetForm('daily_submit')
    monthly_form = BudgetForm('monthly_submit')
    if 'daily_submit' in request.form and daily_form.validate_on_submit():
        amount = daily_form.amount.data
        current_user.daily_budget = amount
        db.session.commit()
    elif 'monthly_submit' in request.form and monthly_form.validate_on_submit():
        amount = monthly_form.amount.data
        current_user.monthly_budget = amount
        db.session.commit()
    elif request.method == 'POST':
        flash('Invalid budget!','danger')
    return render_template('profile.html',user=current_user,daily=daily_form,monthly=monthly_form)

@app.route('/expense',methods=['GET','POST'])
@login_required
def expense():
    expense_form = ExpenseForm()
    if expense_form.validate_on_submit():
        amount = expense_form.amount.data
        place = expense_form.location.data
        date = expense_form.date.data
        time = expense_form.time.data
        datetime = str(date) + ' ' + str(time)
        type = expense_form.type.data
        expense = Expenses(current_user.id,amount,place,datetime,type)
        db.session.add(expense)
        db.session.commit()
        flash('Recorded expense!','success')
        return redirect(url_for('profile'))
    elif request.method == 'POST':
        print(expense_form.errors)
        print(request.form['time'])
        flash('Invalid expense','danger')
    return render_template('expense.html',form=expense_form)
