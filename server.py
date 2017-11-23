from utils.database import Database as db
from utils.authentication import authenticated_resource
from utils.nocache import nocache

from flask import Flask, session, request, flash, redirect, url_for, session
from flask import render_template,abort
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = './data_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
@nocache
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('sign_in'))


@app.route('/<username>', methods=['GET'])
@nocache
def user_url(username):
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        abort(404)


@app.route('/register', methods=['GET', 'POST'])
@nocache
def register():
    if request.method == 'GET':
        return render_template('./register.html', logged_in=False)
    if request.method == 'POST':
        username = (request.form['username']).lower().strip()
        password = (request.form['password'])
        is_valid_username = db.add_user(username, password)
        if is_valid_username.has_key('success'):
            flash(is_valid_username['success'] + '. Sign in now.', 'register_success')
            return redirect(url_for("sign_in"))
        else:
            #print is_valid_username
            flash('Username is already taken', 'register_error')
            return redirect(url_for("register"))

@app.route('/sign_in', methods=['GET', 'POST'])
@nocache
def sign_in():
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('dashboard'))
        return render_template('./sign_in.html', logged_in=False)
    if request.method == 'POST':
        username = (request.form['username']).lower().strip()
        password = (request.form['password'])
        can_login = db.check_can_login(username, password)
        if can_login:
            session['user'] = username
            return redirect(url_for("index"))
        else:
            flash('Invalid username or password', 'sign_in_error')
            return redirect(url_for("sign_in"))


@app.route('/dashboard', methods=['GET'])
@nocache
@authenticated_resource
def  dashboard():
    if request.method == 'GET':
        repositories = [row[1] for row in db.get_repositories(session['user'])]
        return render_template('./dashboard.html',repositories=repositories)

@app.route('/logout', methods=['GET'])
@nocache
def logout():
    if request.method == 'GET':
        session.pop('user', None)
        return redirect(url_for('index'))

# @app.route('/repos/<username>/<repos>')
# def repos(username, repos):
#
@app.route('/add_repositories', methods=['GET', 'POST'])
@nocache
@authenticated_resource
def add_repositories():
    if request.method == 'POST':
        repo_name = (request.form['repo_name']).lower().strip()
        files = request.files.to_dict(flat=False)['files']
        if files:
            print files
            print repo_name
            filefolder = app.config['UPLOAD_FOLDER']+'/'+session['user']+'/'+repo_name+'/'
            for file in files:
                try:
                    os.makedirs(filefolder+'/'.join(file.filename.split('/')[1:-1]))
                    db.add_repositories(repo_name, session['user'])
                except OSError:
                    pass
                file.save(filefolder+'/'.join(file.filename.split('/')[1:]))
            return redirect(url_for('dashboard'))
    return render_template('./add_repositories.html')


if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True, host='0.0.0.0')
