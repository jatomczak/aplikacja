import cx_Oracle


class DbConfiguration:
    def do_configuration(self, db_object):
        db_object.db_user = 'uall'
        db_object.db_password = 'uall'
        db_object.db_name = 'iwh.world'
        db_object.db_connection = 'uall/uall@mnp549.dc.man.lan:1521/mnp549.dc.man.lan'


class UseDb:
    connection = None
    cursor = None
    db_user = ''
    db_password = ''
    db_name = ''
    db_connection = ''

    def __init__(self):
        DbConfiguration().do_configuration(self)

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def send_request(self, request: str):
        self.cursor.execute(request)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


class UseOracleDb(UseDb):
    def __init__(self):
        UseDb.__init__(self)
        self.open_connection()
        self.set_cursor()

    def open_connection(self):
        try:
            self.connection = cx_Oracle.connect(self.db_connection)
        except:
            print("Cannot open %s database" % self.db_connection)

    def set_cursor(self):
        self.cursor = self.connection.cursor()