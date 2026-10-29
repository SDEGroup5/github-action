"""
This module contains the Server class, which implements the IServer interface.
"""

from src.abstraction.i_postgres_connector import IPostgresConnector
from src.abstraction.i_server_handler import IServerHandler


class ServerHandler(IServerHandler):
    """
    A class that implements the IServerHandler interface, links requests to IPostgresConnector
    """

    connector: IPostgresConnector

    def __init__(self, connector: IPostgresConnector):
        self.connector = connector

    def write_number_request_handler(self, number: int) -> int | None:
        '''
        Ask the Postgres connector to write the number.

        If the process succeed, the same number is returned, otherwise None is returned instead
        '''
        return self.connector.write_number(number)

    def read_number_request_handler(self) -> int | None:
        '''
        Ask the Postgres connector to read the current number.
        
        If the process succeed, the number is returned, otherwise None is returned instead
        '''
        return self.connector.get_number()
