import psycopg2
from config import config
from init import init
import sys
import json.decoder
from json_objects import *
from functions import *
from interpreter import *

# more than 2 args:
# arg[0] is the name of the file, 
# arg[1] = '--init', 
# arg[2] is the name of the file with input 

try:
    if len(sys.argv) == 2:
        if(sys.argv[1]=='--init'):
            interpreter()
        else:
            print(ERROR_status('Wrong program argument! The data base is closed'))
    elif len(sys.argv) == 1:
        interpreter()
    else:
        print(ERROR_status(""))

except (Exception, psycopg2.DatabaseError, EOFError) as error:
    print(ERROR_status(str(error)))
