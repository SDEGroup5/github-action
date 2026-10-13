from abstraction.IPostgreConnector import IPostgreConnector
from postgreConnector import PostgreConnector

def main():
    connector: IPostgreConnector = PostgreConnector("localhost","5432","TheDatabase","myuser","secret_password")

    connector.writeNumber(3);
    print(connector.getNumber())

if __name__ == "__main__":
    main()