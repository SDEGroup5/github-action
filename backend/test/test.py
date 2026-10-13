"""
This module contain the test for the PostgreConnector class
"""
from unittest.mock import MagicMock, patch

import psycopg2
from src.abstraction.i_postgre_connector import IPostgreConnector
from src.postgre_connector import PostgreConnector


def test_db_connection_success():
    '''
    Test if a successful database connection is handled correctly
    '''
    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    mock_connection_object = MagicMock()

    with patch("src.postgre_connector.psycopg2.connect",
               return_value=mock_connection_object) as mock_connection:

        result = connector.open_connection()

    assert result is mock_connection_object
    mock_connection.assert_called_once_with(dbname="TheDatabase",
                                            user="myuser",
                                            password="secret_password",
                                            host="localhost",
                                            port="5432")


def test_db_connection_failure():
    '''
    Test if a unsuccessful database connection is handled correctly
    '''
    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    with patch("src.postgre_connector.psycopg2.connect",
               side_effect=psycopg2.OperationalError(
                   "Failed to connect to database")) as mock_connection:
        result = connector.open_connection()

    assert result is None
    mock_connection.assert_called_once_with(dbname="TheDatabase",
                                            user="myuser",
                                            password="secret_password",
                                            host="localhost",
                                            port="5432")
