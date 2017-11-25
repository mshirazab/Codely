import pymysql
# import os
# from werkzeug.security import generate_password_hash, check_password_hash


class Database(object):
    """docstring for Database."""
    db = pymysql.connect(host="localhost", user="root",
                         passwd="sudeep", db="codely")
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
        query = "select * from users where username=\"%s\" and\
        password=\"%s\"" % (username, password)
        done = Database.cursor.execute(query)
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
    def get_user_repos(username):
        Database.cursor.execute("select repo_name from repositories where\
                                 owner=\"%s\"" % (username))
        return Database.cursor.fetchall()

    @staticmethod
    def add_repositories(repo_name, username):
            try:
                query = "insert into repositories(repo_name, owner)\
                 values(\"%s\", \"%s\");" % (repo_name, username)
                Database.cursor.execute(query)
                Database.db.commit()
                return {"success": "Successfully added %s" % (repo_name)}
            except pymysql.err.IntegrityError as e:
                return {"error": e.args[1]}

    @staticmethod
    def check_valid_repo(username, repo_name):
        done = Database.cursor.execute("select repo_name from repositories where\
        owner=\"%s\" and repo_name=\"%s\"" % (username, repo_name))
        if done == 0:
            return False
        return True
