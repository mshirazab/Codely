from database import Database as db
from flask import Flask, session, request, flash, redirect, url_for
# , redirect, url_for, session, request
from flask import render_template
# , abort
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET'])
def index():
    return redirect('/sign_in')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('./register.html', logged_in=False)
    if request.method == 'POST':
        username = (request.form['username']).lower().strip()
        password = (request.form['password'])
        is_valid_username = db.add_user(username, password)
        for key in is_valid_username:
            print key, is_valid_username[key]
        if is_valid_username.has_key('success'):
            flash(is_valid_username['success'] + '. Sign in now.', 'register_success')
            return redirect(url_for("sign_in"))
        else:
            flash('Username is already taken, MF', 'register_error')
            return redirect(url_for("register"))

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('./sign_in.html', logged_in=False)
    if request.method == 'POST':
        username = (request.form['username']).lower().strip()
        password = (request.form['password'])
        can_login = db.check_can_login(username, password)
        if can_login:
            return redirect(url_for("index"))
        else:
            flash(u'Invalid username or password', 'sign_in_error')
            return redirect(url_for("sign_in"))



if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True)
