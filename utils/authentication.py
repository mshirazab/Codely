from flask import redirect, session, url_for, flash
from functools import wraps
from utils.database import Database as db


def authenticated_resource(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)

        return redirect(url_for('sign_in'))

    return decorated


def register(username, password):
    """Register users
    this allows users to register to Codely
    register(username, password) => redirect of flask
    """
    is_valid_username = db.add_user(username, password)
    if 'success' in is_valid_username:
        flash(is_valid_username['success'] + '. Sign in now.',
              'register_success')
        return redirect(url_for("sign_in"))
    else:
        # print is_valid_username
        flash('Username is already taken', 'register_error')
        return redirect(url_for("register"))


def login_in(username, password):
    can_login = db.check_can_login(username, password)
    if can_login:
        session['user'] = username
        return redirect(url_for("index"))
    else:
        flash('Invalid username or password', 'sign_in_error')
        return redirect(url_for("sign_in"))


def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
