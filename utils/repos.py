from utils.database import Database as db
import os
import magic
from flask import redirect, url_for
mime = magic.Magic(mime=True)


class RepositoryHandling:
    @staticmethod
    def get_files(root_path):
        tree = {}
        for path, dirfiles, files, in os.walk(root_path):
            path = path.split('/')[4:]
            path.insert(0, 'root')
            tree['/'.join(path)] = {"files": files, "folders": dirfiles}
        print tree
        return tree

    @staticmethod
    def add_repository(upload_folder, owner, repo_name, files):
        if files:
            print files
            print repo_name
            filefolder = upload_folder + '/'
            filefolder += owner + '/' + repo_name + '/'
            for file in files:
                try:
                    os.makedirs(filefolder+'/'.join(file.filename.split('/')
                                [1:-1]))
                except OSError:
                    pass
                file.save(filefolder+'/'.join(file.filename.split('/')[1:]))
            db.add_repositories(repo_name, owner)
            return redirect(url_for('dashboard'))

    @staticmethod
    def add_commit(filefolder, files):
        if files:
            print files
            for file in files:
                try:
                    os.makedirs(filefolder+'/'.join(file.filename.split('/')
                                [1:-1]))
                except OSError:
                    pass
                file.save(filefolder+'/'.join(file.filename.split('/')[1:]))
            path = '/'.join(filefolder.split('/')[1:])
            print path
            return redirect(url_for('dashboard'))
