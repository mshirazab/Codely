from flask import redirect, session, url_for
from functools import wraps


def authenticated_resource(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)

        return redirect(url_for('sign_in'))

    return decorated
