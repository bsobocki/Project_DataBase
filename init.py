import psycopg2
from config import config

def init(arg): 
    try:
        # connent to the PostgreSQL server
        conn = psycopg2.connect(host='localhost',dbname=arg[0], user=arg[1], password=arg[2])
        # create a new cursor
        cur = conn.cursor()
        # create all components
        cur.execute(open('sql/commands.sql').read())
        # commit changes
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        
    return conn 
