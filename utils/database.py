import pymysql
# import os
# from werkzeug.security import generate_password_hash, check_password_hash


class Database(object):
    """docstring for Database."""
    __db = pymysql.connect(host="localhost", user="root",
                           passwd="sudeep", db="codely")
    __cursor = __db.cursor()

    @staticmethod
    def check_valid_username(username):
        done = Database.__cursor.execute("select * from users where\
                                        username=\"%s\"" % (username))
        if done == 0:
            return False
        return True

    @staticmethod
    def check_can_login(username, password):
        query = "select * from users where username=\"%s\" and\
        password=\"%s\"" % (username, password)
        done = Database.__cursor.execute(query)
        if done == 0:
            return False
        return True

    @staticmethod
    def add_user(username, password):
        try:
            Database.__cursor.execute("insert into users values\
            (\"%s\", \"%s\");" % (username, password))
            Database.__db.commit()
            return {"success": "Successfully signed up as %s" % (username)}
        except pymysql.err.IntegrityError as e:
            return {"error": e.args[1]}

    @staticmethod
    def get_user_repos(username):
        Database.__cursor.execute("select repo_name from repositories where\
                                 owner=\"%s\"" % (username))
        return Database.__cursor.fetchall()

    @staticmethod
    def add_repositories(repo_name, username):
            try:
                query = "insert into repositories(repo_name, owner)\
                 values(\"%s\", \"%s\");" % (repo_name, username)
                Database.__cursor.execute(query)
                Database.__db.commit()
                return {"success": "Successfully added %s" % (repo_name)}
            except pymysql.err.IntegrityError as e:
                return {"error": e.args[1]}

    @staticmethod
    def check_valid_repo(username, repo_name):
        done = Database.__cursor.execute("select repo_name from repositories where\
        owner=\"%s\" and repo_name=\"%s\"" % (username, repo_name))
        if done == 0:
            return False
        return True
