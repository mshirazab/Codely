# from database import Database as db
from flask import Flask
# , redirect, url_for, session, request
from flask import render_template
# , abort
import os
from nocache import nocache
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET'])
@nocache
def index():
    return render_template('./index.html', logged_in=False)


# @app.route('/sign_in', methods=['POST'])
# @nocache
# def sign_in():
#     return render_template('./index.html', logged_in=True)


if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True)
