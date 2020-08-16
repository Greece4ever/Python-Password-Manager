import main
from main import localhost
from getpass import getpass,getuser
from colorama import Fore,Style
import time
from encryption import isNumber
from typing import Union

red = Fore.RED
reset = Style.RESET_ALL
green = Fore.GREEN
blue = Fore.LIGHTBLUE_EX
white = Fore.MAGENTA
red = Fore.RED
yellow = Fore.LIGHTYELLOW_EX

FIELDS_DEMO = {
    "USERNAME" : 1,
    "EMAIL" : 2,
    "PASSWORD" : 3,
    "NAME" : 4,
    "FIRST_NAME" : 5,
    'LAST_NAME' : 6,
    'FULL_NAME' : 7
}


def insert() -> str:
    print(f"\n{blue}[INFO]{reset} ONLY The fields {green}'Platform'{reset} and {green}'password'{reset} are required, anything else may be skipped by hitting enter.\n")
    PLATFORM = input("Platform : ")
    if not len(PLATFORM.strip()) > 0:
        return f'\n{red}[ERROR] "PLATFORM" CANNOT BE EMPTY {reset}'
    USERNAME = input("Username : ")
    EMAIL = input("Email : ")
    PASSWORD = getpass("Password : ")
    if not len(PASSWORD.strip()) > 0:
        return f'\n{red}[ERROR] "PASSWORD" CANNOT BE EMPTY {reset}'
    NAME = input("Name : ")
    FIRST_NAME = input("FIRST_NAME : ")
    LAST_NAME = input("LAST_NAME : ")
    FULL_NAME = input("FULL NAME : ")
    return localhost.add(PLATFORM,PASSWORD,USERNAME,EMAIL,NAME,FIRST_NAME,LAST_NAME,FULL_NAME)


def viewSpecific() -> str:
    print(f"\n{blue}[INFO]{reset} In specific view you must specify the name of the collumn 'Platform' in order to procceed.\n")
    platform = input("Platform : ")
    if not len(platform.strip()) > 0:
        return f'\n{red}[ERROR] "PLATFORM" CANNOT BE EMPTY {reset}\n'
    return localhost.SpecificView(platform)


def viewGeneral() -> str:
    print(f"\n{blue}[INFO]{reset} In General View you can see the list of all the platform you have rows for, in the local db.\n")
    return localhost.GeneralView()


def viewUpdate() -> str:
    print(f"\n{blue}[INFO]{reset} In Update View you can update one or multiple rows by splitting the with commas (,) or by leaving white space beetween them\n")
    print(f"\n{blue}[INFO]{reset} First Specify a {green}'Platform'{reset} to perform the operations, \n")
    platform = input(f"{green}Platform{reset} : ")
    doesExist = localhost.Exists(platform)
    if not doesExist:
            return f'\n{red}[ERROR] ROW DOES NOT EXIST {reset}\n'
    LISTED = list(FIELDS_DEMO)
    for item in FIELDS_DEMO:
        print(f'{red} {LISTED.index(item)} {reset} - {green}{item}{reset}')
    print('\n')
    selected_fields = input(f"Select one or multiple collumns (using {red}number{reset}) by splitting by comma {blue}(,){reset} or space {blue}( ){reset} :")
    selected_fields = [item for item in selected_fields.strip().replace(' ',',').split(',') if item.strip() !='']
    VALUES_TO_UPDATE = []
    for item in selected_fields:
        if not isNumber(item) or int(item) < 0 or int(item) > len(LISTED):
            return f'\n{red}[ERROR] VALUE WAS EITHER NOT A NUMBER OF OUT OF RANGE {reset}\n'
        VALUES_TO_UPDATE.append(LISTED[int(item)])
   
    updated = {}
    for item in VALUES_TO_UPDATE:
        if item.lower() != 'password':
            change = input(f'Update field {blue}{item}{reset} : ')
        else:
            change = getpass(f'Update field {red}{item}{reset} : ')

        updated[item.lower()] = change
    return localhost.Update(doesExist,updated)

def delete() -> str:
    f"\n{yellow}[WARNING]{reset} Any actions done in using the delete() function cannot be undone\n"
    platform = input(f'Type the name of the {green}"Platform"{reset} to delete : ')
    doesExist = localhost.Exists(platform)
    if not doesExist:
            return f'\n{red}[ERROR] ROW DOES NOT EXIST {reset}\n'
    return localhost.delete(doesExist)


ACTIONS = {
    "INSERT" : insert,
    "DELETE" : delete,
    "UPDATE" : viewUpdate,
    "VIEW SPECIFIC" : viewSpecific,
    "VIEW GENERAL" : viewGeneral
}

ACTIONS_LIST = list(ACTIONS)

creator = f"{green}https://github.com/Greece4ever/{reset},"
LINES = f'{green}532{reset},'
VERSION = f"{green}v0.0.1{reset},"
encryption = f'{green}false{reset},'
logging = f'{green}true{reset},'
db = f'{green}local at {getuser()}{reset}'

print(f"{white}<---------------------- PYTHON PASSWORD MANAGER v0.0.1 ---------------------->{reset}")
print("\n")
print(f" {white}< ------- DETAILS  ------- >{reset}\n")
print(" |     {}CREATOR {}:  {} ".format(blue,reset,creator))
print(" |     {}VERSION {}:  {} ".format(blue,reset,VERSION))
print(" |     {}ENCYPTION {}:  {} ".format(blue,reset,encryption))
print(" |     {}LOGGING {}:  {} ".format(blue,reset,logging))
print(" |     {}DATABASE {}:  {} ".format(blue,reset,db))
print(f"\n{white} < ------- [][][][][]  ------- >{reset}")
print('\n')


def main():
    print(f"{white}< ------- Allowed Methods ------- >{reset}\n")
    for index,action in enumerate(ACTIONS):
        print(f'         {red}{index}{reset} - {green}{action}{reset}')
    print(f'\n{white}< ------- [][][][][][][][] ------- >{reset}')
    print("\nSelect one of the following methods by number or by name, \n")

    selected = input(f"{red}Action{reset} to execute : ")
    if not isNumber(selected):
        print(f'\n{red}[ERROR]{reset} value {green}"{selected}"{reset} cannot be interpreted as an integer \n')
        return ValueError("Value cannot be interpreted as an integer")
    selected = int(selected)
    if selected > 4:
        print(f'\n{red}[ERROR]{reset} value {green}"{selected}"{reset} cannot be greater than 4 \n')
        return ValueError("Value cannot be greater than 4")

    selected = int(selected)
    action = ''
    action = ACTIONS_LIST[selected]

    print(f"Executing {red}action{reset} {action}...")
    print(ACTIONS.get(action)())
    input(f"\nPress {green}Enter{reset} to Continue : \n")

while True:
    main()