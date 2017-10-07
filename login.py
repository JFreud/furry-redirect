from flask import Flask, render_template, request, session, redirect, url_for
import os

echo_app = Flask(__name__)

echo_app.secret_key = os.urandom(32)

#dictionary, keys are usernames, values are passwords
logins = dict()
logins["username"] = "password"

@echo_app.route("/", methods = ["GET", "POST"])
def root():
    try:
        #if session already exists: redirect to welcome page
        if session["username"] in logins.keys() and session["password"] == logins[session["username"]]:
            return redirect(url_for("welcome", logged = "true"))
        #if it exists, but the login is wrong, then display error message:
        else:
            session.clear()
            return render_template('base.html', error = "Incorrect username or password")
    #session doesn't exist yet:
    except KeyError:
        return render_template('base.html')

@echo_app.route("/welcome/", methods = ["GET", "POST"])
def welcome():
    #print request.form
    #print request.args
    #if already logged in:
    if "logged" in request.args:
        try:
            return render_template("welcome.html", user = session["username"])
        #if people try to go directly to the url:
        except KeyError:
            return redirect(url_for('root'))
    #creates new session with correct login:
    username = request.form["username"]
    password = request.form["password"]
    session["username"] = username
    session["password"] = password
    if username in logins.keys() and password == logins[username]:
        return render_template("welcome.html", user = username)
    return redirect(url_for('root'))

@echo_app.route("/logout/")
def logout():
    #clears session and sends back to login page:
    session.clear()
    return redirect(url_for('root'))





if __name__ == "__main__":
    echo_app.debug = True
    echo_app.run()
