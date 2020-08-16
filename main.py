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
from colorama import Fore,Style
import encryption


red = Fore.RED
reset = Style.RESET_ALL
green = Fore.GREEN
blue = Fore.LIGHTBLUE_EX
white = Fore.MAGENTA
red = Fore.RED
ligthred = Fore.LIGHTRED_EX

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
            print("\n {}[INFO]{} CREATED DATABASE [{}] \n".format(blue,reset,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            connection.commit()
        except sqlite3.OperationalError:
            print("\n {}[INFO]{} Detected local database at {}{}{} \n".format(blue,reset,green,os.getcwd(),reset))

    def __str__(self):
        return f'Local sqlite3 db at path {self.path}'

    def add(self,platform : str,password : str,username : Union[str,bool] = NULL,email : Union[str,bool] = NULL,name : Union[str,bool] = NULL,first_name : Union[str,bool] = NULL,last_name : Union[str,bool] = NULL,full_name : Union[str,bool]=NULL):
        try:
            connection.execute(
                """
                INSERT INTO DATA VALUES (:platform,:date,:password,:username,:email,:name,:first_name,:last_name,:full_name)
            """,{
                "platform" : platform if platform.split() !='' else None,
                "date" : time.time(),
                "username" : username if username.split() !='' else None,
                "password" : password if password.split() !='' else None,
                "email" : email if email.split() !='' else None,
                "name" : name if name.split() !='' else None,
                "first_name" : first_name if first_name.split() !='' else None,
                "last_name" : last_name if last_name.split() !='' else None,
                "full_name" : full_name if full_name.split() !='' else None
            })
            logging.log(LEVELS[0],"INSERTED {}".format(platform))
            connection.commit()
            logging.log(LEVELS[0],"INSERTED ROW {}".format(platform))
            return f'{blue}[INFO]{reset} Successfully inserted info at row {green}{platform}{reset}.'
        except sqlite3.IntegrityError:
            logging.log(LEVELS[2],"FAILED TO INSERT {} (ALREADY EXISTS)".format(platform))
            return f'\n{red}[{LEVELS[-1]}]{reset} Platform {green}{platform}{reset} has already been declared!'

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
        return f'{red}[{LEVELS[1]}]{reset} Deleted ALL on platform {green}{platform}{reset}'

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
                    ORDER BY date_created DESC

                """,[f'%{platform}%']
            )
            result = queryset.fetchall()
            length = len(result)
            if not length > 0:
                return f'{red}[ERROR] No results for the platform{reset} {green}"{platform}"{reset}.'
            else:
                DATA = {}
                INFO = []
                print(f"There were {red}{length}{reset} results")
                for index,item in enumerate(result):
                    DATA[index+1] = item
                    INFO.append(f'{red}{index+1}{reset} - {green}{item[0]}{reset}')
                print("\n".join(INFO))
                print(f"Select by specifying the corresponding {red}number{reset}")
                num = input()
                if not encryption.isNumber(num):
                    print(f'{red}[ERROR] Invalid Argument{reset} {green}"{num}"{reset}{red} is not a number{reset}')
                    return self.SpecificView(platform)
                return self.SpecificView(DATA[int(num)][0])


        result = result[0]
        username = result[2]
        email = result[3]
        name = result[4]
        first_name = result[5]
        last_name = result[6]
        full_name = result[7]      
        u1 = f'{blue} USERNAME {reset}: {green} {username} {reset}'
        e1 = f'{blue} EMAIL {reset}: {green} {email} {reset}'
        n1 = f'{blue} NAME {reset}: {green} {name} {reset}'
        f1 = f'{blue} FIRST NAME {reset}: {green} {first_name} {reset}'
        l1 = f'{blue} LAST NAME {reset}: {green} {last_name} {reset}'
        fu1 = f'{blue} FULL NAME {reset}: {green} {full_name} {reset}'
        EMPTY = ''
        TIME = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        t_1 = time.time()
        TIME_DIFFERENCE = t_1 - t_0
        res = f"""
       {white} ----------------------------------------------------- {reset}
               {ligthred} PLATFORM {reset}:{green} {result[0]}{reset}
               {u1 if username is not None and username.strip() != '' else EMPTY}
               {e1 if email is not None and email.strip() != '' else EMPTY}
                {blue}PASSWORD {reset}:{green} {result[1]}{reset}      
               {n1 if name is not None and name.strip() != '' else EMPTY}
               {f1 if first_name is not None and first_name.strip() != '' else EMPTY}
               {l1 if last_name is not None and  last_name.strip() != ''else EMPTY}
               {fu1 if full_name is not None and full_name.strip() != '' else EMPTY}

            Succesfully ended query - {TIME}    
        {white} -----------------------------------------------------{reset}
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
            ORDER BY date_created DESC
            """
        )
        data = data.fetchall()
        INFO = [length,[(info[0],info[1]) for info in data]]
        #wtf
        VISUAL_DATA = [f'{red}{INFO[1].index(item)}{reset} - {blue}{item[0].upper()}{reset} : {red}{item[1]}{reset} {green}CHARACTERS{reset}' for item in INFO[1]]
        t_1 = time.time()
        HEAD = f"""
{white}< ----------------------------------------------------- >{reset}
{blue}TOTAL NUMBER OF ROWS IN DATABASE{reset} : {green}{INFO[0]}{reset}
        """
        LIST = [HEAD]
        for item in VISUAL_DATA:
            LIST.append(item)
        TIME = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        TIME_DIFFERENCE = t_1 - t_0
        BOTTOM = f"""
Succesfully ended query in {green}{TIME_DIFFERENCE}s{reset} - {TIME} 
{white}< ----------------------------------------------------- >{reset}
        """
        LIST.append(BOTTOM)
        logging.log(LEVELS[0],"QUERY FOR * finished in {}".format(TIME_DIFFERENCE))
        print("\n".join(LIST))
        num = input(f"Select a {red}number{reset} to Perform a query for : ")
        print("\n\n\n")
        if not encryption.isNumber(num):
            return f'{red}[ERROR] Invalid argument "{num}" is not a number {reset}'
        num = int(num)
        LENGTH = len(INFO[1])
        if (num > LENGTH or num < 0):
            return f'{red}[ERROR] Invalid argument "{num}" is out of list range (MAX : {LENGTH}) {reset}'
        res = str(INFO[1][num][0])
        return self.SpecificView(res)
        
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
        data = ",".join([f'{item.upper()}' for item in updated])
        msg = f'{blue}[INFO]{reset} Successfully updated rows for platofrm {blue}{RESP[0]}{reset} : {green}{data}{reset}.'
        logging.log(LEVELS[0],msg)
        return f'{msg}'
    
    def Exists(self,platform : str) -> bool:
        data = connection.execute("""
            SELECT platform FROM DATA WHERE UPPER(platform) = UPPER(?)
        """,(platform,))
        data = data.fetchall()
        try:
            resp = data[0][0]
            return resp
        except:
            return False

localhost = Database()

if __name__ == "__main__":
    pass