import psycopg2
from config import config

def delete_data():
        try:
                # read the connection parameters
                params = config('files/database.ini')

                # connent to the PostgreSQL server
                conn = psycopg2.connect(**params)

                # create a new cursor
                cur = conn.cursor()

                cur.execute(open('sql/delete.sql').read())

                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
                print(error)

        conn.close()
        
delete_data()