import psycopg2
from psycopg2 import connect
from configparser import ConfigParser

class dbConnection:
    def __init__(self, filename='/app/db/database.ini', section='postgresql'):
        self.parser = ConfigParser() 
        self.parser.read(filename)   
        self.db = {}   
        self.conn = None

        if self.parser.has_section(section):
            self.params = self.parser.items(section)
            for param in self.params:
                self.db[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} can\'t be found in {filename} file.")

    def connect(self):
        try:
            self.conn = psycopg2.connect(host = self.db['host'], 
                                        database = self.db['database'], 
                                        user = self.db['user'], 
                                        password = self.db['password'],
                                        port = self.db['port']
                                        )
        except (Exception, psycopg2.DatabaseError) as err: 
            print(f"Database connection error:  {err}")
    
    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
        self.conn = None

    def commit(self):
        self.conn.commit()

    def execute(self, query, args=None):
        if self.conn is None or self.conn.closed:
            self.connect()
        curs = self.conn.cursor()
        try:
            curs.execute(query, args)
        except Exception as ex:
            self.conn.rollback()
            curs.close()
            raise ex
        return curs   

    def fetchall(self, query, args=None):
        curs = self.execute(query, args)
        rows = curs.fetchall()
        curs.close()
        return rows
