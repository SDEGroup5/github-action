"""
Placeholder
"""

from abc import ABC, abstractmethod

import psycopg2


class IPostgreConnector(ABC):

    @abstractmethod
    def open_connection(self, addr: str, port: str, db_name: str, username: str,
                       psw: str) -> psycopg2.extensions.connection | None:
        '''Implement connection method.

        Should return the connection if successful, otherwise None.
        '''

    @abstractmethod
    def write_number(self, number: int) -> int | None:
        '''Write the specified number to the database.

        Should return the number itself if it was written, otherwise None.
        '''

    @abstractmethod
    def get_number(self) -> int | None:
        '''Return the number from the database, or None if unsuccessful.'''

    @abstractmethod
    def close_connection(self, conn: psycopg2.extensions.connection) -> bool:
        '''Return True if the connection was successfully closed, otherwise False.'''
