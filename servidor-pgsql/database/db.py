import psycopg2
from os import environ
from dotenv import load_dotenv
from psycopg2 import DatabaseError

load_dotenv()


def get_connection():
    try:
        return psycopg2.connect(
            host=environ.get('DB_HOST'),
            port=environ.get('DB_PORT'),
            user=environ.get('DB_USER'),
            password=environ.get('DB_PASSWORD'),
            dbname=environ.get('DB_NAME')
        )
    except DatabaseError as ex:
        raise ex
