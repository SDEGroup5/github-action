"""
This module contain the test for the PostgreConnector class
"""

import json
import threading
from functools import partial
from http.client import HTTPConnection, HTTPResponse
from http.server import HTTPServer
from unittest.mock import MagicMock, patch

import psycopg2
import pytest  # pylint: disable=import-error
from src.abstraction.i_postgre_connector import IPostgreConnector
from src.abstraction.i_server_handler import IServerHandler
from src.postgre_connector import PostgreConnector
from src.server import Server
from src.server_handler import ServerHandler

# PostgreConnector tests


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


def test_db_write_number_failure_on_connection():
    '''
    Test whether the postgre connector is correctly handling a read
    request when the connection to the database was not successful
    '''

    value_to_write: int = 1

    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    with patch("src.postgre_connector.psycopg2.connect",
               side_effect=psycopg2.OperationalError(
                   "Failed to connect to database")) as mock_connection:
        result = connector.write_number(value_to_write)

    assert result is None
    mock_connection.assert_called_once_with(dbname="TheDatabase",
                                            user="myuser",
                                            password="secret_password",
                                            host="localhost",
                                            port="5432")


def test_db_write_number_failure_on_writing():
    '''
    Test whether the postgre connector is correctly able to ask the
    database to write a number. The function should return None
    '''
    value_to_write: int = 1

    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    mock_connection_object = MagicMock()

    mock_connection_object.cursor.return_value.execute.side_effect = psycopg2.DatabaseError(
        "Error")

    with patch("src.postgre_connector.psycopg2.connect",
               return_value=mock_connection_object) as mock_connection:
        result = connector.write_number(value_to_write)

    assert result is None
    mock_connection.assert_called_once_with(dbname="TheDatabase",
                                            user="myuser",
                                            password="secret_password",
                                            host="localhost",
                                            port="5432")


def test_db_write_number_successful():
    '''
    Test whether the postgre connector is correctly able to ask the
    database to write a number. The function should return the same
    number that should be written
    '''
    value_to_write: int = 1

    connector: IPostgreConnector = PostgreConnector(
        "localhost",
        "5432",
        "TheDatabase",
        "myuser",
        "secret_password",
    )

    mock_connection_object = MagicMock()

    mock_connection_object.cursor.return_value.execute.return_value = None

    with patch("src.postgre_connector.psycopg2.connect",
               return_value=mock_connection_object) as mock_connection:
        result = connector.write_number(value_to_write)

    assert result == value_to_write

    mock_connection_object.cursor.return_value.execute.assert_called_once()
    mock_connection.assert_called_once_with(dbname="TheDatabase",
                                            user="myuser",
                                            password="secret_password",
                                            host="localhost",
                                            port="5432")


def test_db_get_number_successful():
    '''
    Test whether the postgre connector is able to correctly return
    the value from the database. Suppose the current number is 1.
    '''
    desired_value: int = 1

    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    mock_connection_object = MagicMock()

    # Mock the result returned by the cursor fetchone function
    mock_connection_object.cursor.return_value.__enter__.return_value.fetchone.return_value = (
        desired_value, )

    # Patch of the connection still necessary
    with patch("src.postgre_connector.psycopg2.connect",
               return_value=mock_connection_object) as mock_connection:
        result = connector.get_number()

    assert result == desired_value
    mock_connection.assert_called_once_with(dbname="TheDatabase",
                                            user="myuser",
                                            password="secret_password",
                                            host="localhost",
                                            port="5432")


def test_db_get_number_failure_on_connection():
    '''
    Test whether the postgre connector is able handle a reading with
    no connection.
    '''
    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    with patch("src.postgre_connector.psycopg2.connect",
               side_effect=psycopg2.OperationalError(
                   "Failed to connect to database")) as mock_connection:
        result = connector.get_number()

    assert result is None
    mock_connection.assert_called_once_with(dbname="TheDatabase",
                                            user="myuser",
                                            password="secret_password",
                                            host="localhost",
                                            port="5432")


def test_db_get_number_failure_on_reading():
    '''
    Test whether the postgre connector is correctly able to ask the
    database to write a number. The function should return None
    '''

    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    mock_connection_object = MagicMock()

    mock_cursor = mock_connection_object.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.side_effect = psycopg2.DatabaseError("Error")

    with patch("src.postgre_connector.psycopg2.connect",
               return_value=mock_connection_object) as mock_connection:
        result = result = connector.get_number()

    assert result is None
    mock_connection.assert_called_once_with(dbname="TheDatabase",
                                            user="myuser",
                                            password="secret_password",
                                            host="localhost",
                                            port="5432")


def test_db_get_number_failure_on_read_result():
    '''
    Test whether the postgre connector is able handle a reading with no results.
    '''

    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    mock_connection_object = MagicMock()

    # Mock the result returned by the cursor fetchone function
    mock_connection_object.cursor.return_value.__enter__.return_value.fetchone.return_value = None

    # Patch of the connection still necessary
    with patch("src.postgre_connector.psycopg2.connect",
               return_value=mock_connection_object) as mock_connection:
        result = connector.get_number()

    assert result is None
    mock_connection.assert_called_once_with(dbname="TheDatabase",
                                            user="myuser",
                                            password="secret_password",
                                            host="localhost",
                                            port="5432")


# ServerHandler tests


def test_server_handler_write():
    '''
    Test if the server handler correctly return the result returned
    by the mock PostgreConnector in case of write
    '''
    value_to_write: int = 1

    connector = MagicMock()

    connector.write_number.return_value = value_to_write

    sh: IServerHandler = ServerHandler(connector)

    result = sh.write_number_request_handler(value_to_write)

    assert result == value_to_write


def test_server_handler_read():
    '''
    Test if the server handler correctly return the result returned
    by the mock PostgreConnector in case of read
    '''
    desired_value: int = 1

    connector = MagicMock()

    connector.get_number.return_value = desired_value

    sh: IServerHandler = ServerHandler(connector)

    result = sh.read_number_request_handler()

    assert result == desired_value


# Server tests


def test_server_get_successful():
    '''
    Test if the server component is able to answer correctly to a
    GET request. Suppose the database has value desired_value
    '''

    desired_value: int = 1

    server_handler_mock = MagicMock()

    server_handler_mock.read_number_request_handler.return_value = desired_value

    server_partial: partial[Server] = partial(
        Server, server_handler=server_handler_mock)

    server = HTTPServer(("127.0.0.1", 8000), server_partial)

    # Run the server in another thread to avoid blocking the current test
    server_thread: threading.Thread = threading.Thread(
        target=server.serve_forever)

    # Start the thread with the server
    server_thread.start()

    # Prepare the header

    header: dict = {
        "Content-Type": "application/json",
    }

    con: HTTPConnection = HTTPConnection("127.0.0.1", 8000)
    con.request("GET", "/number", headers=header)

    response: HTTPResponse = con.getresponse()

    con.close()

    # Shutdown server and end the thread
    server.shutdown()
    server.server_close()
    server_thread.join()

    assert json.loads(response.read().decode("utf-8")) == {
        "number": desired_value
    }
    assert response.status == 200


@pytest.mark.parametrize(
    "endpoint, mocked_return, expected_status, expected_response",
    [("/number", None, 500, {
        "error": "Internal error"
    }), ("/nonExistent", 1, 404, {
        "error": "Not found"
    })],
)
def test_server_get_failure(endpoint: str, mocked_return: int | None,
                            expected_status: int, expected_response: dict):
    '''
    Test various kind of failures during a GET request to the Server
    component
    '''

    server_handler_mock = MagicMock()

    server_handler_mock.read_number_request_handler.return_value = mocked_return

    server_partial: partial[Server] = partial(
        Server, server_handler=server_handler_mock)

    server = HTTPServer(("127.0.0.1", 8000), server_partial)

    # Run the server in another thread to avoid blocking the current test
    server_thread: threading.Thread = threading.Thread(
        target=server.serve_forever)

    # Start the thread with the server
    server_thread.start()

    # Prepare the header
    header: dict = {
        "Content-Type": "application/json",
    }

    con: HTTPConnection = HTTPConnection("127.0.0.1", 8000)
    con.request("GET", endpoint, headers=header)

    response: HTTPResponse = con.getresponse()

    con.close()

    # Shutdown server and end the thread
    server.shutdown()
    server.server_close()
    server_thread.join()

    assert json.loads(response.read().decode("utf-8")) == expected_response
    assert response.status == expected_status


def test_server_put_success():
    '''
    Test if the server component is able to answer correctly to a
    PUT request
    '''

    value_to_write: int = 1

    server_handler_mock = MagicMock()

    server_handler_mock.write_number_request_handler.return_value = value_to_write

    server_partial: partial[Server] = partial(
        Server, server_handler=server_handler_mock)

    server = HTTPServer(("127.0.0.1", 8000), server_partial)

    # Run the server in another thread to avoid blocking the current test
    server_thread: threading.Thread = threading.Thread(
        target=server.serve_forever)

    # Start the thread with the server
    server_thread.start()

    # Prepare the header and the body

    data: dict = {"number": value_to_write}
    request: bytes = json.dumps(data).encode("utf-8")
    header: dict = {
        "Content-Type": "application/json",
        "Content-Length": str(len(request))
    }

    con: HTTPConnection = HTTPConnection("127.0.0.1", 8000)
    con.request("PUT", "/number", headers=header, body=request)

    response: HTTPResponse = con.getresponse()

    con.close()

    # Shutdown server and end the thread
    server.shutdown()
    server.server_close()
    server_thread.join()

    assert json.loads(response.read().decode("utf-8")) == {
        "success": value_to_write
    }
    assert response.status == 200


@pytest.mark.parametrize(
    "endpoint, value_to_write, mocked_return, expected_status, expected_response",
    [("/number", 1, None, 500, {
        "error": "Internal error"
    }), ("/nonExistent", 1, 1, 404, {
        "error": "Not found"
    })],
)
def test_server_put_failure(endpoint: str, value_to_write: int,
                            mocked_return: int | None, expected_status: int,
                            expected_response: dict):
    '''
    Test various kind of failures during a PUT request to the Server
    component
    '''

    server_handler_mock = MagicMock()

    server_handler_mock.write_number_request_handler.return_value = mocked_return

    server_partial: partial[Server] = partial(
        Server, server_handler=server_handler_mock)

    server = HTTPServer(("127.0.0.1", 8000), server_partial)

    # Run the server in another thread to avoid blocking the current test
    server_thread: threading.Thread = threading.Thread(
        target=server.serve_forever)

    # Start the thread with the server
    server_thread.start()

    # Prepare the header and the body

    data: dict = {"number": value_to_write}
    request: bytes = json.dumps(data).encode("utf-8")
    header: dict = {
        "Content-Type": "application/json",
        "Content-Length": str(len(request))
    }

    con: HTTPConnection = HTTPConnection("127.0.0.1", 8000)
    con.request("PUT", endpoint, headers=header, body=request)

    response: HTTPResponse = con.getresponse()

    con.close()

    # Shutdown server and end the thread
    server.shutdown()
    server.server_close()
    server_thread.join()

    assert json.loads(response.read().decode("utf-8")) == expected_response
    assert response.status == expected_status
