import psycopg2
from config import config

def init(arg): 
    try:
        conn = psycopg2.connect(host='localhost',dbname=arg[0], user=arg[1], password=arg[2])
        cur = conn.cursor()
        cur.execute(open('sql/commands.sql').read())
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        
    return conn 
