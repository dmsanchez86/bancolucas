import psycopg2
import urllib.parse as urlparse
import os


class DBHelper():
    def connect(self):
        # ----- config database ---------
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS accounts (num_account integer, name_user text, account_balance integer);")
        cur.execute("CREATE TABLE IF NOT EXISTS commands (num_user integer, command text);")
        return conn


    # create account bank user
    def create_account(self, num_account, name_user, account_balance):
        connection = self.connect()
        try:
            query = "INSERT INTO accounts (num_account, name_user, account_balance) VALUES (%s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account, name_user, account_balance,))
                connection.commit()
        finally:
            connection.close()


    # A user has an account
    def account_exists(self, num_account):
        connection = self.connect()
        try:
            query = "SELECT * FROM accounts WHERE num_account = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account,))
                if cursor.fetchone() is None:
                    return False
                else:
                    return True
        finally:
            connection.close()

    # show account of user

    def show_account(self, num_account):
        connection = self.connect()
        try:
            query = "SELECT * FROM accounts WHERE num_account = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account,))
                return cursor.fetchone()
        finally:
            connection.close()

    # delete account
    def delete_account(self, num_account):
        connection = self.connect()
        try:
            query = "DELETE FROM accounts WHERE num_account = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account,))
                connection.commit()
        finally:
            connection.close()

    def user_exists(self, num_user):
        connection = self.connect()
        try:
            query = "SELECT * FROM commands WHERE num_user = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_user,))
                if cursor.fetchone() is None:
                    return False
                else:
                    return True
        finally:
            connection.close()

    def add_command(self, num_user, command):
        connection = self.connect()
        try:

            if self.user_exists(num_user) == False:
                query_insert = "INSERT INTO commands (num_user, command) VALUES (%s, %s);"
                with connection.cursor() as cursor:
                    cursor.execute(query_insert, (num_user, command,))
                    cursor.close()
                    connection.commit()

            else:
                query_update = 'UPDATE commands SET command = %s WHERE num_user = %s'
                with connection.cursor() as cursor:
                    cursor.execute(query_update, (command, num_user,))
                    cursor.close()
                    connection.commit()
        finally:
            connection.close()



    # def ultimate_command(self, num_user):
    #     connection = self.connect()
    #     try:
    #         query = "SELECT * FROM commands WHERE num_user = %s"
    #         with connection.cursor() as cursor:
    #             cursor.execute(query, (num_user,))
    #             return cursor.fetchone()
    #     finally:
    #         connection.close()