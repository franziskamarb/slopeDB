import psycopg2
from psycopg2 import Error

PGHOST = 'localhost'
PGDATABASE = 'SlopeDB'
PGUSER = 'postgres'
PGPASSWORD = 'jamubo01'

conn_string = "host="+PGHOST+" port="+"5432"+" dbname="+PGDATABASE+ \
            " user="+PGUSER +  " password="+PGPASSWORD
conn=psycopg2.connect(conn_string)

try:
    cur = conn.cursor()
    query1 = ('SELECT * FROM "ACCOMODATION";')
    cur.execute(query1)
    employees = cur.fetchall()
    for e in employees:
        print(e)
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()