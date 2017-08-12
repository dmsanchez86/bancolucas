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
        return conn


    # create account bank user
    def create_account(self, num_account, name_user, account_balance):
        connection = self.connect()
        try:
            query = "INSERT INTO tasks (num_account, name_user, account_balance) VALUES (%s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account, name_user, account_balance))
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

