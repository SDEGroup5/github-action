from abc import ABC, abstractmethod
import psycopg2

class IPostgreConnector():
    @abstractmethod
    def openConnection(self, addr: str, port: str, dbName: str, username:str, psw: str) -> psycopg2.extensions.connection  | None:
        '''Implement connection method. Should return postgre connection object. Should return the connection if connection was succesfull, otherwise None'''

    @abstractmethod
    def writeNumber(self, number: int) -> int | None:
        '''Write the specified number to the database. Should return the number itself if it was written, otherwise None'''

    @abstractmethod
    def getNumber(self) -> int | None:
        '''Return the number from the database. If not succesfull, None should be returned instead'''

    @abstractmethod
    def closeConnection(self, conn: psycopg2.extensions.connection) -> bool:
        '''Should return true if connection was succesfully closed, false otherwise'''