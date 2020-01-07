from app import app
import requests

if __name__ == '__main__':
    app.run(debug=True)

# if logged in: welcome page, else login page
@app.route("/", methods=['GET', 'POST'])
def home():
    if 'user' in session: #checks that a user is logged into a session, render welcome page
        print("Session username: " + session['user'])
        flash ("You are logged in.")
        print(session['user'])
        return render_template("base.html", username = str(session['user']))

    return render_template("login.html") #if not, then render login page

# login page
@app.route("/auth", methods=['POST'])
def login():
    username = request.form.get('user')
    password = request.form.get('pw')

    #if (db_ops.authenticate(username, password)):
    #    session['user'] = username
    #    return redirect(url_for('home')) #should trigger if statement in "/" route

    flash("Failed to log in. The username or password provided did not match any accounts.")
    return redirect(url_for('home'))

# signup route redirects to the register page template
@app.route("/signup")
def signup():
    return render_template("register.html")

# register for a new account page
@app.route("/register", methods=['POST'])
def register():
    username = request.form.get('user')
    password = request.form.get('pw')

    #if (db_ops.accountExists(username)):
    #    flash("This username is already in use. Try another one.")
    #    return redirect(url_for('signup'))

    #db_ops.addAccount(username, password)
    #flash("You have successfully created your account. Please log in now.")
    return redirect(url_for('home'))
