from flask import Flask, render_template, request, session
from app.models import db, Users, Expenses

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
