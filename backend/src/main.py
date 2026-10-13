"""
Main file
"""

from abstraction.i_postgre_connector import IPostgreConnector
from postgre_connector import PostgreConnector


def main():
    """Main function for testing purposes."""

    connector: IPostgreConnector = PostgreConnector("localhost", "5432",
                                                    "TheDatabase", "myuser",
                                                    "secret_password")

    connector.write_number(3)

    print(connector.get_number())


if __name__ == "__main__":
    main()
