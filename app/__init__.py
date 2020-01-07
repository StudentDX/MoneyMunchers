from flask import Flask, render_template, request, session
from app.models import db, Users, Expenses

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return render_template('home.html')
@app.route('/home')
def home():
    return render_template('home.html')
