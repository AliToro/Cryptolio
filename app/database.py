import logging
import os

import psycopg2
from fastapi import HTTPException


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

    def get_price(self, coin_token, epoc):
        self.cur.execute("""
        select epoc, price 
        from (
            select * 
            from currency_price 
            where currency='{coin_token}' and abs(epoc - {epoc}) < 30*86400
        ) as n 
        order by abs(epoc - {epoc}) 
        limit 1
        """.format(coin_token=coin_token, epoc=epoc))
        logging.info("The number of parts: {}".format(self.cur.rowcount))
        if self.cur.rowcount == 0:
            message = "Cannot find any price for {coin_token} near to {epoc}".format(coin_token=coin_token, epoc=epoc)
            logging.warning(message)
            raise HTTPException(status_code=503, detail=message)
        else:
            row = self.cur.fetchone()
            logging.info("The closest epoc and price are: {}".format(row))
            return row


pg_connector = MyPsycopg2Connector()
