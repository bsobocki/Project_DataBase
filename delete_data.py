import psycopg2
from config import config

def delete_data():
        try:
                params = config('files/database.ini')
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(open('sql/delete.sql').read())
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        conn.close()
        
delete_data()
