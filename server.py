from utils.database import Database as db
from utils.authentication import authenticated_resource
import utils.authentication as auth
from utils.nocache import nocache
from utils.repos import RepositoryHandling as rh

from flask import Flask, session, request, redirect, url_for
from flask import render_template, abort
import os
import magic

mime = magic.Magic(mime=True)
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


@app.route('/register', methods=['GET', 'POST'])
@nocache
def register():
    if request.method == 'POST':
        username = (request.form['username']).lower().strip()
        password = (request.form['password'])
        return auth.register(username, password)
    return render_template('./register.html', logged_in=False)


@app.route('/sign_in', methods=['GET', 'POST'])
@nocache
def sign_in():
    if request.method == 'POST':
        username = (request.form['username']).lower().strip()
        password = (request.form['password'])
        return auth.login_in(username, password)
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('./sign_in.html', logged_in=False)


@app.route('/logout', methods=['GET'])
@nocache
def logout():
    return auth.logout()


@app.route('/dashboard', methods=['GET'])
@nocache
@authenticated_resource
def dashboard():
    if request.method == 'GET':
        repositories = [row[0] for row in db.get_user_repos(session['user'])]
        return render_template('./dashboard.html', repositories=repositories)


@app.route('/add_repositories', methods=['GET', 'POST'])
@nocache
@authenticated_resource
def add_repositories():
    if request.method == 'POST':
        repo_name = (request.form['repo_name']).lower().strip()
        files = request.files.to_dict(flat=False)['files']
        return rh.add_repository(app.config['UPLOAD_FOLDER'],
                                 session['user'], repo_name, files)
    return render_template('./add_repositories.html')


@app.route('/<username>/<path:path>', methods=['GET'])
@nocache
def repositories(username, path):
    repo_name = path.split('/')[0]
    if db.check_valid_repo(username, repo_name):
        req_path = app.config['UPLOAD_FOLDER'] + '/'
        req_path += username + '/'
        req_path += path
        tree = rh.get_files(req_path)
        return render_template('./repositories.html', tree=tree)
    else:
        abort(404)


@app.route('/file/<path:path>', methods=['GET'])
@nocache
def file_display(path):
    path = app.config['UPLOAD_FOLDER'] + '/' + path
    if 'text' in mime.from_file(path):
        code = ""
        with open(path, "r") as fp:
            for line in fp:
                code += line
        return render_template('./print_text_file.html', code=code)
    else:
        print mime.from_file(path)
        abort(404)


@app.route('/add_commit/<path:path>', methods=['POST'])
@nocache
@authenticated_resource
def add_commit(path):
    path = app.config['UPLOAD_FOLDER'] + '/' + path + '/'
    files = request.files.to_dict(flat=False)['file']
    # shutil.rmtree(path)
    rh.add_commit(path, files)
    return path


if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True, host='0.0.0.0')
