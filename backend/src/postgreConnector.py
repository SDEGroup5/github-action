from src.abstraction.IPostgreConnector import IPostgreConnector

import psycopg2

class PostgreConnector(IPostgreConnector):
    addr: str
    port: str
    dbName: str
    username:str
    psw: str

    def __init__(self,addr: str, port: str, dbName: str, username:str, psw: str):
        self.addr=addr
        self.port=port
        self.dbName=dbName
        self.username=username
        self.psw=psw

    def openConnection(self) -> psycopg2.extensions.connection | None:
        try:
            return psycopg2.connect(dbname=self.dbName,user=self.username,password=self.psw,host=self.addr,port=self.port)
        except (psycopg2.DatabaseError,Exception) as err:
            print(err)
            return None

    def writeNumber(self, number: int) -> int | None:
        query: str = "UPDATE NumberTable SET number=(%s) WHERE NumberIndex=0"

        
        conn: psycopg2.extensions.connection | None = self.openConnection()

        if (conn is None):
            return None
        
            
        try:
            conn.cursor().execute(query,(str(number)))
            return number
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            self.closeConnection(conn)

    def getNumber(self) -> int | None:
        query: str = "SELECT Number FROM NumberTable WHERE NumberIndex=0"
        
        conn: psycopg2.extensions.connection | None = self.openConnection()

        if (conn is None):
            return None

        try:
            with conn.cursor() as curs:
                curs.execute(query)
                single_row = curs.fetchone()

                if single_row is None:
                    return None

                return single_row[0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            self.closeConnection(conn)

    def closeConnection(self, conn: psycopg2.extensions.connection) -> bool:
        conn.close()
        return True
        