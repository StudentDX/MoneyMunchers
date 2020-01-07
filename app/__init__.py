from flask import Flask, render_template, request, session

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')
@app.route('/home')
def home():
    return render_template('home.html')
