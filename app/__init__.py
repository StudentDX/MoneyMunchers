from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for, flash
from app.models import db, Users, Expenses, Exchanges
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from functools import wraps
from datetime import date, timedelta
from sqlalchemy import and_

from app.forms import SignUpForm, LogInForm, BudgetForm, ExpenseForm
from app.exchange_rates import update_rates

app = Flask(__name__)

app.config['SECRET_KEY'] = urandom(64)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

currencies = []
db.init_app(app)
with app.app_context():
    db.create_all()
    update_rates()
    currencies = [[e.currency,e.symbol] for e in Exchanges.query.all()]

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

def get_symbol():
    return Exchanges.query.filter_by(id=current_user.currency_id).first().symbol

def to_money(amount):
    exchange = Exchanges.query.filter_by(id=current_user.currency_id).first()
    exchanged = round(amount * exchange.rate,2)
    if amount < 0:
        return '-'+exchange.symbol+str(exchanged)[1:]+('0' if str(exchanged)[-2] == '.' else '')
    else:
        return exchange.symbol + str(exchanged) + ('0' if str(exchanged)[-2] == '.' else '')

app.jinja_env.filters['to_money'] = to_money
app.jinja_env.globals.update(get_symbol=get_symbol)
app.jinja_env.globals.update(list=list)
app.jinja_env.globals.update(currencies=currencies)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/')
@app.route('/home')
def home():
    print(request.endpoint)
    return render_template('home.html')

@app.route('/help.html')
def help():
    return render_template('help.html')

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
    if current_user.daily_budget is not None:
        if current_user.daily_balance() < 10 and current_user.daily_balance() > 0:
            flash('You are close to exceeding your daily budget.', 'warning')
        if current_user.daily_balance() < 0:
            flash('You have exceeded your daily budget.', 'danger')
    if current_user.monthly_budget is not None:
        if current_user.monthly_balance() < 10 and current_user.monthly_balance() > 0:
            flash('You are close to exceeding your monthly budget.', 'warning')
        if current_user.monthly_balance() < 0:
            flash('You have exceeded your monthly budget.', 'danger')
    daily_form = BudgetForm('daily_submit')
    monthly_form = BudgetForm('monthly_submit')
    if 'currency' in request.form:
        current_user.currency_id = Exchanges.query.filter_by(currency=request.form['currency']).first().id
        db.session.commit()
    elif 'daily_submit' in request.form and daily_form.validate_on_submit():
        amount = daily_form.amount.data
        rate = Exchanges.query.filter_by(id=current_user.currency_id).first().rate
        amount = float(amount) / rate
        current_user.daily_budget = amount
        db.session.commit()
    elif 'monthly_submit' in request.form and monthly_form.validate_on_submit():
        amount = monthly_form.amount.data
        rate = Exchanges.query.filter_by(id=current_user.currency_id).first().rate
        amount = float(amount) / rate
        if current_user.daily_budget is not None and amount < current_user.daily_budget:
            flash('Monthly budget cannot be less than daily budget!','danger')
        else:
            current_user.monthly_budget = amount
            db.session.commit()
    elif request.method == 'POST':
        flash('Invalid budget!','danger')
    return render_template('profile.html',user=current_user,daily=daily_form,monthly=monthly_form)

@app.route('/expense',methods=['GET','POST'])
@login_required
def expense():
    expense_form = ExpenseForm()
    if 'currency' in request.form:
        current_user.currency_id = Exchanges.query.filter_by(currency=request.form['currency']).first().id
        db.session.commit()
    elif expense_form.validate_on_submit() or (len(expense_form.errors)==1 and 'time' in expense_form.errors and request.form['time'][-2:] == '00'):
        amount = expense_form.amount.data
        rate = Exchanges.query.filter_by(id=current_user.currency_id).first().rate
        amount = float(amount) / rate
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
        flash('Invalid expense','danger')
    return render_template('expense.html',form=expense_form)

@app.route('/trends',methods=['GET','POST'])
@login_required
def trends():
    time = 'Past Week'
    if 'currency' in request.form:
        current_user.currency_id = Exchanges.query.filter_by(currency=request.form['currency']).first().id
        db.session.commit()
    elif 'time' in request.form:
        time = request.form['time']
    today = date.today()
    if 'Past' in time:
        if 'Week' in time:
            start = today - timedelta(weeks=1)
        elif 'Month' in time:
            if today.month > 1:
                start = today.replace(month=today.month - 1)
            else:
                start = today.replace(month=12, year=today.year - 1)
        elif 'Year' in time:
            start = today.replace(today.year - 1)
        query = Expenses.query.filter(and_(Expenses.date.between(str(start), str(date.today()+timedelta(days=1)))),Expenses.user_id==current_user.id)
        time = 'in the ' + time
    else:
        query = Expenses.query.filter_by(user_id=current_user.id)
        time = 'of ' + time
    history = {}
    for entry in query:
        if entry.date[:10] not in history:
            history[entry.date[:10]] = entry.amount
        else:
            history[entry.date[:10]] += entry.amount
    return render_template('trends.html',time=time,history=history)
