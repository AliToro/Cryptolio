import logging
import os

import psycopg2


class MyPsycopg2Connector():
    def __init__(self):
        self.user = os.environ['cryptolio_db_user']
        self.password = os.environ['cryptolio_db_password']
        self.host = os.environ['cryptolio_db_host']
        self.database = os.environ['cryptolio_db_dbname']
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # connect to the PostgreSQL server
            logging.info('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(user=self.user, password=self.password, host=self.host, database=self.database)

            # create a cursor
            self.cur = self.conn.cursor()

            # execute a statement
            logging.debug('PostgreSQL database version:')
            self.cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = self.cur.fetchone()
            logging.debug(db_version)

            logging.info("... Connected successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            logging.critical("Exception in creating connection: ", error)
            raise error

    def close(self):
        try:
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.critical("Exception: ", error)
            raise error
        finally:
            if self.conn is not None:
                self.conn.close()
                logging.info('Database connection closed.')

    def get_data(self):
        self.cur.execute("SELECT * FROM kucoin_btc_usd_hourly limit 10")
        logging.info("The number of parts: {}".format(self.cur.rowcount))
        row = self.cur.fetchone()

        while row is not None:
            logging.info(row)
            row = self.cur.fetchone()


pg_connector = MyPsycopg2Connector()
