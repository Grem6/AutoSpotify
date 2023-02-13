import configparser
from colorama import init
init(autoreset=False)
YELLOW = "\x1b[1;33;40m"
RED = "\x1b[1;31;40m"

def authen_create():
    
    print(f"\n{YELLOW}paste your client id here: ",end='')
    client_id = input(RED)
    print(f"\n{YELLOW}paste your client secret id here: ",end='')
    client_secret = input(RED)
    auth = configparser.ConfigParser()
    auth['credentials'] = {"client_id": client_id, "client_secret": client_secret}

    with open('auth.conf', 'w') as configfile:
        auth.write(configfile)
        
