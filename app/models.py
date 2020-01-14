from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
    daily_budget = db.Column(db.Float)
    monthly_budget = db.Column(db.Float)

    expenses = db.relationship('Expenses',backref='user')

    def __init__(self,username,password):
        self.username = username
        self.password = password

class Expenses(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    user_id = db.Column(db.ForeignKey('users.id'))
    amount = db.Column(db.Float,nullable=False)
    place = db.Column(db.String(80))
    date = db.Column(db.Text)
    type = db.Column(db.String(80))

    def __int__(self,user,amount):
        self.user = user
        self.amount = amount