import psycopg2
from config import config
from init import init
import sys
import json.decoder
from json_objects import *
from functions import *
from interpreter import *

try:
    ### more than 2 args (arg[0] is name of this file, arg[1] is --init, arg[2] is the name if the file with input) ###
    if len(sys.argv) == 2:
        # if exist an argument --init 
        if(sys.argv[1]=='--init'):
            # run interpreter
            interpreter()
        else:
            print(ERROR_status('Wrong program argument! The data base is closed'))

    ### run program without --init ### 
    elif len(sys.argv) == 1:
        # run interpreter
        interpreter()
    else:
        print(ERROR_status(""))

except (Exception, psycopg2.DatabaseError, EOFError) as error:
    print(ERROR_status(str(error)))
