import cx_Oracle
import configparser
import sqlite3


class UseDb:
    connection = None
    cursor = None
    db_user = ''
    db_password = ''
    db_name = ''

    def __init__(self, config_section: str):
        DbConfiguration(config_section).do_configuration(self)

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def send_request(self, request: str):
        self.cursor.execute(request)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


class DbConfiguration:

    def __init__(self, config_section: str):
        self.config = configparser.ConfigParser()
        self.config_section = config_section
        try:
            self.config.read('properties.cfg')

        except configparser.Error:
            print('Nie mozna odnaelzc pliku')

    def do_configuration(self, db_object):
        try:
            db_object.db_user = self.get_db_user()
            db_object.db_password = self.get_db_password()
            db_object.db_name = self.get_db_name()

        except configparser.NoOptionError:
            print("Plik konfiguracyjny zostal uszkodzony")

    def get_db_user(self):
        return self.config.get(self.config_section, 'user')

    def get_db_password(self):
        return self.config.get(self.config_section, 'password')

    def get_db_name(self):
        return self.config.get(self.config_section, 'database_name')


class UseOracleDb(UseDb):

    def __init__(self):
        UseDb.__init__(self, 'KAST_SQL')
        self.open_connection()
        self.set_cursor()

    def open_connection(self):
        try:
            self.connection = cx_Oracle.connect(self.db_user, self.db_password, self.db_name)
        except:
            print("Cannot open %s database" % self.db_name)

    def set_cursor(self):
        self.cursor = self.connection.cursor()


class UseLocalDb(UseDb):
    def __init__(self):
        UseDb.__init__(self, 'LOCAL_DB')
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()