from django.test import TestCase
from .oracle_db import UseOracleDb

import time
from functools import wraps


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

class OkbvTest(TestCase):
    @timethis
    def test_oracle_with_query(self):
        with UseOracleDb() as cursor:
            cursor.execute("select * from Beom.iwh_aufwaende where lub_nr ='79778'")
            result = cursor.fetchall()

    @timethis
    def test_oracle_db_2(self):
        with UseOracleDb() as cursor:
            pass


# Create your tests here.
