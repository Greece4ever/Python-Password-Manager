import sqlite3
import os
import logger

connection = sqlite3.connect('psdb.db')
logging = logger.Logger(f"{os.getcwd()}\\logs.log")

LEVELS = [
    'INFO',
    'WARNING',
    'ERROR'
]

NULL = None

class Database:
    def __init__(self):
        try:
            connection.execute('''
                CREATE TABLE DATA (
                    platform text NOT NULL UNIQUE,
                    password text,
                    username text NULL,
                    email text NULL,
                    name text NULL,
                    first_name text NULL,
                    last_name text NULL,
                    full_name text NULL
                );
            ''')
            logging.log(LEVELS[0],"CREATED DATABASE")
            connection.commit()
        except sqlite3.OperationalError:
            print("Detected local database at {}".format(os.getcwd()))

    def add(self,platform,password,username=NULL,email=NULL,name=NULL,first_name=NULL,last_name=NULL,full_name=NULL):
        connection.execute(
            """
            INSERT INTO DATA VALUES (:platform,:password,:username,:email,:name,:first_name,:last_name,:full_name)
        """,{
            "platform" : platform,
            "username" : username,
            "password" : password,
            "email" : email,
            "name" : name,
            "first_name" : first_name,
            "last_name" : last_name,
            "full_name" : full_name
        })
        logging.log(LEVELS[0],"INSERTED {}".format(platform))
        connection.commit()

    def delete(self,platform):
        connection.execute(
            """
            DELETE FROM DATA WHERE platform = ?
            """
        ,(platform,))
        logging.log(LEVELS[1],"DELETED {}".format(platform))
        connection.commit()

    def view(self,platform):
        connection.execute("""
            SELECT platform FROM DATA
        """)



localhost = Database()
localhost.add("Twitter","peos")

