import psycopg2
from psycopg2 import DatabaseError


def get_connection():
    try:
        return psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='postgres',
            dbname='inventary'
        )
    except DatabaseError as ex:
        raise ex
