"""
Main file
"""

from functools import partial
from http.server import HTTPServer

from src.abstraction.i_postgre_connector import IPostgreConnector
from src.abstraction.i_server_handler import IServerHandler
from src.postgre_connector import PostgreConnector
from src.server import Server
from src.server_handler import ServerHandler


def main():
    """Main function for testing purposes."""

    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    server_handler: IServerHandler = ServerHandler(connector)

    server_partial: partial[Server] = partial(Server,
                                              server_handler=server_handler)

    server = HTTPServer(("127.0.0.1", 8000), server_partial)

    server.serve_forever()


if __name__ == "__main__":
    main()
