from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
    daily_budget = db.Column(db.Float)
    monthly_budget = db.Column(db.Float)
    currency_id = db.Column(db.ForeignKey('exchanges.id'))

    currency = db.relationship('Exchanges')
    expenses = db.relationship('Expenses',backref='user')

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.currency_id = 11

    def daily_balance(self):
        balance = self.daily_budget
        for expense in [e for e in self.expenses if e.date[:10] == str(date.today())]:
            balance -= expense.amount
        return balance

    def monthly_balance(self):
        balance = self.monthly_budget
        for expense in [e for e in self.expenses if e.date[:7] == str(date.today())[:7]]:
            balance -= expense.amount
        return balance

    def get_currency(self):
        return Exchanges.query.filter_by(id=self.currency_id).first().currency

class Expenses(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    user_id = db.Column(db.ForeignKey('users.id'))
    amount = db.Column(db.Float,nullable=False)
    place = db.Column(db.String(80))
    date = db.Column(db.Text)
    type = db.Column(db.String(80))

    def __init__(self,user_id,amount,place,date,type):
        self.user_id = user_id
        self.amount = amount
        self.place = place
        self.date = date
        self.type = type

class Exchanges(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    currency = db.Column(db.String(3),nullable=False,unique=True)
    symbol = db.Column(db.String(1),nullable=False)
    rate = db.Column(db.Float,nullable=False)

    def __init__(self,currency,symbol,rate):
        self.currency = currency
        self.symbol = symbol
        self.rate = rate