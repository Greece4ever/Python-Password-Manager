"""
    -----------------------------------------------
    CURRENT SQL TABLE FORMAT :
        platform UNIQUE NOT NULL
        date_created integer NOT NULL
        password text
        username
        email
        name
        first_name
        last_name
        full_name
    -----------------------------------------------

"""

import sqlite3
import os
import logger
import datetime
import time
from typing import Union

connection = sqlite3.connect('psdb.db')
# connection.set_trace_callback(print)


logging = logger.Logger(os.path.join(os.getcwd(),"logs"))

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
                    date_created integer NOT NULL, 
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
            print("[INFO] CREATED DATABASE [{}]".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            connection.commit()
        except sqlite3.OperationalError:
            print("[INFO] Detected local database at {}".format(os.getcwd()))

    def __str__(self):
        return f'Local sqlite3 db at path {self.path}'

    def add(self,platform : str,password : str,username : Union[str,bool] = NULL,email : Union[str,bool] = NULL,name : Union[str,bool] = NULL,first_name : Union[str,bool] = NULL,last_name : Union[str,bool] = NULL,full_name : Union[str,bool]=NULL):
        try:
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
            logging.log(LEVELS[0],"INSERTED ROW {}".format(platform))
            return f'[INFO] Successfully added inserted row {platform}.'
        except sqlite3.IntegrityError:
            logging.log(LEVELS[2],"FAILED TO INSERT {} (ALREADY EXISTS)".format(platform))
            return f'[{LEVELS[-1]}] Platform {platform} has already been declared!'

    def delete(self,platform :str):
        f = connection.execute(
            'SELECT * FROM DATA where platform = ?',(platform,)
        )
        __all__ = f.fetchall()
        if not len(__all__) > 0:
            logging.log(LEVELS[2],"FAILED TO DELETE {} (NO RESULTS)".format(platform))
            return f'[ERROR] Query came up with no results, and thus makeing deletion not feasible.'

        connection.execute(
            """
            DELETE FROM DATA WHERE platform = ?
            """
        ,(platform,))
        logging.log(LEVELS[1],"DELETED {}".format(platform))
        connection.commit()
        return f'[{LEVELS[1]}] Deleted ALL on platform {platform}'

    def quickQuery(self):
        """
            Returns the first collumn (platform UNIQUE NOT NULL) of all rows
        """
        data = connection.execute(
            """
            SELECT platform FROM DATA
            """
        )
        return [platform[0] for platform in data.fetchall()]

    def SpecificView(self,platform : str) -> str:
        """
            Given a string input it querys the DATA table to see if there is any row such that:
            => input == platform
        """

        t_0 = time.time()
        queryset = connection.execute("""
            SELECT * FROM DATA WHERE platform = ?
        """,(platform,))

        result = queryset.fetchall()
        if not len(result) > 0:
            logging.log(LEVELS[2],"QUERY FOR '{}' returned no results".format(platform,)) 
            logging.log(LEVELS[0],"EXECUTING CASE INSENSITIVE-LIKE QUERY FOR {}".format(platform,)) 
            queryset = connection.execute(
                """
                    SELECT * FROM DATA WHERE UPPER(platform) like UPPER(?)
                """,[f'%{platform}%']
            )
            result = queryset.fetchall()
            length = len(result)
            if not length > 0:
                return '[ERROR] No results for the platform "{}".'.format(platform) 
            else:
                DATA = {}
                INFO = []
                print("There were {} results".format(length))
                for index,item in enumerate(result):
                    DATA[index+1] = item
                    INFO.append(f'{index+1} - {item[0]}')
                print("\n".join(INFO))
                print("Select by specifying the corresponding number")
                num = input()
                return self.SpecificView(DATA[int(num)][0])


        result = result[0]
        username = result[2]
        email = result[3]
        name = result[4]
        first_name = result[5]
        last_name = result[6]
        full_name = result[7]      
        u1 = f' USERNAME : {username}'
        e1 = f' EMAIL : {email}'
        n1 = f' NAME : {name}'
        f1 = f' FIRST NAME : {first_name}'
        l1 = f' LAST NAME : {last_name}'
        fu1 = f' FULL NAME : {full_name}'
        EMPTY = ''
        TIME = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        t_1 = time.time()
        TIME_DIFFERENCE = t_1 - t_0
        res = f"""
        -----------------------------------------------------
                PLATFORM : {result[0]}
               {u1 if username is not None else EMPTY}
               {e1 if email is not None else EMPTY}
                PASSWORD : {result[1]}      
               {n1 if name is not None else EMPTY}
               {f1 if first_name is not None else EMPTY}
               {l1 if last_name is not None else EMPTY}
               {fu1 if full_name is not None else EMPTY}

            Succesfully ended query - {TIME}    
        -----------------------------------------------------
        """.split("\n")
        res = [item for item in res if item.strip() !='']
        res[-2] = f'\n {res[-2]}' 
        logging.log(LEVELS[0],"QUERY FOR '{}' finished in {}".format(platform,TIME_DIFFERENCE))
        return "\n".join(res)

    def GeneralView(self) -> str:
        t_0 = time.time()
        length = connection.execute(
            """
            SELECT COUNT(platform) FROM DATA
            """
        )
        length = length.fetchall()[0][0]
        data = connection.execute(
            """
            SELECT platform,LENGTH(password) FROM DATA
            """
        )
        data = data.fetchall()
        INFO = [length,[(info[0],info[1]) for info in data]]
        #wtf
        VISUAL_DATA = [f'             {item[0].upper()} : {item[1]} CHARACTERS' for item in INFO[1]]
        t_1 = time.time()
        HEAD = f"""
        -----------------------------------------------------
            TOTAL NUMBER OF ROWS IN DATABASE : {INFO[0]}
        """
        LIST = [HEAD]
        for item in VISUAL_DATA:
            LIST.append(item)
        TIME = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        TIME_DIFFERENCE = t_1 - t_0
        BOTTOM = f"""
        Succesfully ended query in {TIME_DIFFERENCE}s - {TIME} 
        -----------------------------------------------------   
        """
        LIST.append(BOTTOM)
        logging.log(LEVELS[0],"QUERY FOR * finished in {}".format(TIME_DIFFERENCE))
        return "\n".join(LIST)
    
    def Update(self,platform : str,updated : dict) -> str:
        """
        => Method that updates all specifeid collumns of  a single row
        => You pass in a string platform : The UNIQUE NOT NULL collumn
        => You pass in a dict updated : specifying what you want to update
        Example :
                    {
                        'username' : 'Elon',
                        'password' : 'mars'
                    }

            I cannot just select the rows I want from user input
            so I have to make 2 querys getting all the data
            and if something is blank, setting it the the fecthed
            data from the first query
        """


        #Make query to get length of data and the data in case a field is blank
        RESP = connection.execute(
            """
            SELECT * FROM DATA
            WHERE platform = ?
            """
        ,(platform,))

        RESP = RESP.fetchall()

        if not len(RESP) > 0:
            msg = f'Specified row "{platform}" could not be found.'
            logging.log(LEVELS[2],msg)
            return f'[{LEVELS[2]}] {msg}'

        RESP = RESP[0]
        BEFORE = {
            "password" : RESP[1],
            "username" : RESP[2],
            "email" : RESP[3],
            "name" : RESP[4],
            "first_name" : RESP[5],
            "last_name" : RESP[6],
            "full_name" : RESP[7] 
        }

        connection.execute(
            """
            UPDATE DATA
            SET  password = :password,username = :username,email = :email,name = :name,first_name = :first_name,last_name = :last_name, full_name = :full_name
            WHERE platform = :platform
            """
        ,{
            "platform" : platform,
            "password" : updated['password'] if 'password' in updated else BEFORE["password"],
            "username" : updated['username'] if 'username' in updated else BEFORE["username"],
            "email" : updated['email'] if 'email' in updated else BEFORE["email"],
            "name" : updated['name'] if 'name' in updated else BEFORE["name"],
            "first_name" : updated['first_name'] if 'first_name' in updated else BEFORE["first_name"],
            "last_name" : updated['last_name'] if 'last_name' in updated else BEFORE["last_name"],
            "full_name" : updated['full_name'] if 'full_name' in updated else BEFORE["full_name"],
        })     

        connection.commit()
        data = "".join([f'{item.upper()}' for item in updated])
        msg = f'Successfully updated rows for platofrm {RESP[0]} : {data} .'
        logging.log(LEVELS[0],msg)
        return f'[INFO] {msg}'


localhost = Database()
print(localhost.add("Youtube","chanlder","MrBeast"))
print(localhost.add("YouPorn","arab","MiaKhalifa"))
print(localhost.SpecificView("you"))