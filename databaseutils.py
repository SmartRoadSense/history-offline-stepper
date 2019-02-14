#!/usr/bin/python
import psycopg2
from config import raw_config
from config import agg_config
import datetime

# DB Constants
SINGLE_DATA_TABLE = "single_data"
SINGLE_DATA_DATE_COLUMN = "date"
ARCHIVE = "archive"


def connect(db='raw'):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = raw_config() if db == 'raw' else agg_config()

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


def empty_out_single_data(conn):
    try:
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute('TRUNCATE {};'.format(SINGLE_DATA_TABLE))

        print("Table {0} has been cleaned out.".format(SINGLE_DATA_TABLE))

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise Exception


def move_data_within_time_frame(conn, tf):
    try:
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute('INSERT INTO {0} SELECT * FROM {1} WHERE {1}.{2} > \'{3}\' '
                    'AND {1}.{2} < \'{4}\';'.format(SINGLE_DATA_TABLE, ARCHIVE, SINGLE_DATA_DATE_COLUMN, tf[0], tf[1]))

        print("Table {0} populated.".format(SINGLE_DATA_TABLE))

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise Exception


def save_current_to_history(conn, time_frame, limit='50000000'):
    try:
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute('SELECT srs_current_to_history({0}, {1});'.format(limit, time_frame))

        print("History saved as time-frame: {0}.".format(time_frame))

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise Exception


def get_osm_ids(conn):
        try:
            # create a cursor
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # execute a statement
            cur.execute('SELECT osm_line_id FROM single_data WHERE osm_line_id IS NOT NULL GROUP BY osm_line_id;')

            rows = cur.fetchall()

            osm_ids = []

            for row in rows:
                osm_ids.append(row['osm_line_id'])

            print(osm_ids)

            # close the communication with the PostgreSQL
            cur.close()

            return osm_ids

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise Exception


