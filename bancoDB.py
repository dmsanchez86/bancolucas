# -*- coding: utf-8 -*-
import psycopg2
import urllib.parse as urlparse
import os
import datetime

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
        cur.execute("CREATE TABLE IF NOT EXISTS accounts (num_account integer, "
                    "name_user text, account_balance integer, state bool);")
        cur.execute("CREATE TABLE IF NOT EXISTS transfers "
                    "(id serial PRIMARY KEY, num_account_sender integer, "
                    "num_account_receive integer, account_balance integer, "
                    "date DATE, state bool);")
        cur.execute("CREATE TABLE IF NOT EXISTS withdraw "
                    "(id serial PRIMARY KEY, num_account integer, "
                    "last_account_balance integer, current_account_balance integer, "
                    "total_withdraw integer, date DATE, state bool);")
        return conn


    # create account bank user
    def create_account(self, num_account, name_user, account_balance, state):
        connection = self.connect()
        try:
            query = "INSERT INTO accounts (num_account, name_user, account_balance, state) VALUES (%s, %s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account, name_user, account_balance, state,))
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

    # desactivate account
    def desactivate_account(self, num_account):
        connection = self.connect()
        try:
            query = "UPDATE accounts SET state = False WHERE num_account = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account,))
                connection.commit()
        finally:
            connection.close()

    def activate_account(self, num_account):
        connection = self.connect()
        try:
            query = "UPDATE accounts SET state = True WHERE num_account = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account,))
                connection.commit()
        finally:
            connection.close()

    def add_balance(self, deposit, num_account):
        connection = self.connect()
        try:

            query = "UPDATE accounts SET account_balance = %s WHERE num_account = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (deposit, num_account,))
                connection.commit()
        finally:
            connection.close()

    def withdraw(self, amount, num_account):
        connection = self.connect()
        try:
            query = "UPDATE accounts SET account_balance = %s WHERE num_account = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (amount, num_account,))
                connection.commit()
        finally:
            connection.close()

    def withdraw_new(self, num_account, last_balance, current_balance, total_withdraw, state):
        connection = self.connect()
        try:
            query = "INSERT INTO withdraw (num_account, " \
                    "last_account_balance, current_account_balance, total_withdraw, date, state) " \
                    "VALUES (%s, %s, %s, %s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account, last_balance, current_balance, total_withdraw, datetime.date.today(), state,))
                connection.commit()
        finally:
            connection.close()

    # get withdraws by account
    def get_withdraws(self, num_account):
        connection = self.connect()
        try:
            query = "SELECT * from withdraw WHERE num_account = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account,))
                return cursor.fetchone()
        finally:
            connection.close()

    # get balance account
    def get_balance(self, num_account):
        connection = self.connect()
        try:
            query = "SELECT account_balance from accounts WHERE num_account = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account,))
                return cursor.fetchone()
        finally:
            connection.close()

    # transfer money to other account
    def transfer_to_account(self, num_account_sender, num_account_receive, account_balance, state):
        connection = self.connect()
        try:
            query = "INSERT INTO transfers (num_account_sender, " \
                    "num_account_receive, account_balance, date, state) " \
                    "VALUES (%s, %s, %s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account_sender, num_account_receive, account_balance, datetime.date.today(), state,))
                connection.commit()
        finally:
            connection.close()

    # get transfers sends by num account
    def get_transfers_sends(self, num_account):
        connection = self.connect()
        try:
            query = "SELECT * FROM transfers WHERE num_account_sender = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account,))
                return cursor.fetchall()
        finally:
            connection.close()

    # get transfers receives by num account
    def get_transfers_receive(self, num_account):
        connection = self.connect()
        try:
            query = "SELECT * FROM transfers WHERE num_account_receive = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (num_account,))
                return cursor.fetchall()
        finally:
            connection.close()

