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
