"""
This module contains the PostgreConnector class, which implements the IPostgreConnector interface.
"""

import psycopg2  # pylint: disable=import-error
from src.abstraction.i_postgre_connector import IPostgreConnector


class PostgreConnector(IPostgreConnector):
    """
    A class that implements the IPostgreConnector interface for connecting to a PostgreSQL database.
    """
    addr: str
    port: str
    db_name: str
    username: str
    psw: str

    def __init__(self, addr: str, port: str, db_name: str, username: str,
                 psw: str):
        self.addr = addr
        self.port = port
        self.db_name = db_name
        self.username = username
        self.psw = psw

    def open_connection(self) -> psycopg2.extensions.connection | None:
        '''
        Implement connection method.
        Should return the connection if successful, otherwise None.
        '''
        try:
            return psycopg2.connect(dbname=self.db_name,
                                    user=self.username,
                                    password=self.psw,
                                    host=self.addr,
                                    port=self.port)
        except (psycopg2.DatabaseError, Exception) as err:  # pylint: disable=broad-except
            print(err)
            return None

    def write_number(self, number: int) -> int | None:
        """
        Write the specified number to the database.
        Returns the number if successful, otherwise None.
        """
        query: str = "UPDATE NumberTable SET number=(%s) WHERE NumberIndex=0"

        conn: psycopg2.extensions.connection | None = self.open_connection()

        if conn is None:
            return None

        try:
            conn.cursor().execute(query, (str(number)))
            return number
        except (Exception, psycopg2.DatabaseError) as error:  # pylint: disable=broad-except
            print(error)
            return None
        finally:
            self.close_connection(conn)

    def get_number(self) -> int | None:
        """
        Return the number from the database, or None if unsuccessful.
        """
        query: str = "SELECT Number FROM NumberTable WHERE NumberIndex=0"

        conn: psycopg2.extensions.connection | None = self.open_connection()

        if conn is None:
            return None

        try:
            with conn.cursor() as curs:
                curs.execute(query)
                single_row = curs.fetchone()

                if single_row is None:
                    return None

                return single_row[0]
        except (Exception, psycopg2.DatabaseError) as error:  # pylint: disable=broad-except
            print(error)
            return None
        finally:
            self.close_connection(conn)

    def close_connection(self, conn: psycopg2.extensions.connection) -> bool:
        '''Return True if the connection was successfully closed, otherwise False.'''
        conn.close()
        return True
