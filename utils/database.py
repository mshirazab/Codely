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
    def check_valid_repo(username, repo_name):
        done = Database.__cursor.execute("select repo_name from repositories where\
        owner=\"%s\" and repo_name=\"%s\"" % (username, repo_name))
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
    def add_repositories(repo_name, username):
            try:
                query = "insert into repositories(repo_name, owner)\
                 values(\"%s\", \"%s\");" % (repo_name, username)
                Database.__cursor.execute(query)
                Database.__db.commit()
                return {"success": "Successfully added %s" % (repo_name)}
            except pymysql.err.IntegrityError as e:
                return {"error": e.args[1]}

    # add data in collaborators
    @staticmethod
    def add_collaborators(repo_id, username):
        # this check can be avoid if we give add collaborator option
        # from users who are only present in the db.
        # Has to be implemented in the front end.
        user_exists = Database.check_valid_username(username)
        if user_exists is False:
            return "This user is not registered and \
hence can not be a collaborator"
        try:
            query = "insert into collaborators values\
            (\"%s\", %d);" % (username, repo_id)
            Database.__cursor.execute(query)
            Database.__db.commit()
            return "Successfully added %s" % (username)
        except pymysql.err.IntegrityError:
            return "Collaborator addition failed"

    # add data in tags
    @staticmethod
    def add_tags(repo_id, tag):
        try:
            query = "insert into tags values(%d, \"%s\");" % (repo_id, tag)
            Database.__cursor.execute(query)
            Database.__db.commit()
            return {"success": "Successfully added %d to %s" % (tag, repo_id)}
        except pymysql.err.IntegrityError:
            return "Tag addition failed"

    # adding data in commit
    @staticmethod
    def add_commit(username, repo_id):
        try:
            # current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            query = "insert into commits(username, repo_id) values\
            (\"%s\",%d);" % (username, repo_id)
            # passing time as string to the database, verify its working.
            Database.__cursor.execute(query)
            Database.__db.commit()
            return "Successfully committed"
        except pymysql.err.IntegrityError:
            return "Commit failed"

    # get data from collaborators
    @staticmethod
    def get_collaborators(repo_id):
        query = "select username from collaborators \
        where repo_id=%d" % (repo_id)
        Database.__cursor.execute(query)
        return Database.__cursor.fetchall()

    @staticmethod
    def get_user_repos(username):
        Database.__cursor.execute("select repo_name from repositories where\
                             owner=\"%s\"" % (username))
        return Database.__cursor.fetchall()

    # get data from commits
    @staticmethod
    def get_commits(repo_id):
        query = "select username,commit_time from \
        repositories where repo_id=%d order by commit_time" % (repo_id)
        Database.__cursor.execute(query)
        return Database.__cursor.fetchall()

    # get data from repositories
    @staticmethod
    def get_tags(repo_id):
        ''' get tags from database
        '''
        query = "select topic from tags where repo_id=%d" % (repo_id)
        Database.__cursor.execute(query)
        return Database.__cursor.fetchall()

    @staticmethod
    def get_repo_id(repo_name, username):
        done = Database.__cursor.execute("select repo_id from repositories where\
        owner=\"%s\" and repo_name=\"%s\"" % (username, repo_name))
        if done == 0:
            return False
        return Database.__cursor.fetchall()[0][0]
