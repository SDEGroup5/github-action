from unittest.mock import patch, MagicMock
from  src.abstraction.IPostgreConnector import IPostgreConnector
from src.postgreConnector import PostgreConnector

import psycopg2

def testDbConnectionSuccess():
    connector: IPostgreConnector = PostgreConnector("localhost","5432","TheDatabase","myuser","secret_password")

    mockConnection = MagicMock()

    with patch(
        "src.postgreConnector.psycopg2.connect",
        return_value=mockConnection
    ) as mock_connection:

        result = connector.openConnection()

    assert result is mockConnection
    mock_connection.assert_called_once_with(
        dbname="TheDatabase",
        user="myuser",
        password="secret_password",
        host="localhost",
        port="5432"
    )

def testDbConnectionFailure():
    connector: IPostgreConnector = PostgreConnector("localhost","5432","TheDatabase","myuser","secret_password")

    with patch(
        "src.postgreConnector.psycopg2.connect",
        side_effect=psycopg2.OperationalError("Failed to connect to database")
    ) as mock_connection:
        result = connector.openConnection()
        
    assert result is None
    mock_connection.assert_called_once_with(
        dbname="TheDatabase",
        user="myuser",
        password="secret_password",
        host="localhost",
        port="5432"
    )