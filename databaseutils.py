#!/usr/bin/python
import psycopg2
from config import config
import datetime


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def disconnect(conn):
    if conn is not None:
        conn.close()
        print('Database connection closed.')


def get_date_range(conn):
    # TODO: real general purpose implementation
    begin = datetime.date(2016, 1, 1)
    end = datetime.date(2019, 2, 5)

    return [begin, end]