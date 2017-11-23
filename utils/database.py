import pymysql
# import os
# from werkzeug.security import generate_password_hash, check_password_hash


class Database(object):
    """docstring for Database."""
    db = pymysql.connect(host="localhost", user="root",
                         passwd="mohak666", db="codely")
    cursor = db.cursor()

    @staticmethod
    def check_valid_username(username):
        done = Database.cursor.execute("select * from users where\
                                        username=\"%s\"" % (username))
        if done == 0:
            return False
        return True

    @staticmethod
    def check_can_login(username, password):
        done = Database.cursor.execute("select * from users where\
                                        username=\"%s\" and password=\"%s\"" % (username, password))
        if done == 0:
            return False
        return True

    @staticmethod
    def add_user(username, password):
        try:
            Database.cursor.execute("insert into users values(\"%s\", \"%s\");"
                                    % (username, password))
            Database.db.commit()
            return {"success": "Successfully signed up as %s" % (username)}
        except pymysql.err.IntegrityError as e:
            return {"error": e.args[1]}

    @staticmethod
    def get_repositories(username):
        Database.cursor.execute("select * from repositories where\
                                 owner=\"%s\"" % (username))
        return Database.cursor.fetchall()

    @staticmethod
    def add_repositories(repo_name, username):
            try:
                Database.cursor.execute("insert into repositories(repo_name, owner) values(\"%s\", \"%s\");"
                                        % (repo_name, username))
                Database.db.commit()
                return {"success": "Successfully signed up as %s" % (username)}
            except pymysql.err.IntegrityError as e:
                return {"error": e.args[1]}
