"""
Contains IServerHandler interface, links requests with IPostgresConnector
"""

from abc import ABC, abstractmethod


class IServerHandler(ABC):
    '''
    IServer interface, links requests with IPostgresConnector
    '''

    @abstractmethod
    def write_number_request_handler(self, number: int) -> int | None:
        '''
        Ask the Postgres connector to write the number.

        If the process succeed, the same number is returned, otherwise None is returned instead
        '''

    @abstractmethod
    def read_number_request_handler(self) -> int | None:
        '''
        Ask the Postgres connector to read the current number.
        
        If the process succeed, the number is returned, otherwise None is returned instead
        '''
