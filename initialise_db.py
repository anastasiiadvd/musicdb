#import packages to allow a connection to the postgreSQL database and to catch its error messages
import psycopg2
import psycopg2.errors

#connect to the default postgres database (replace YOUR_PASSWORD_HERE with your own password)
conn = psycopg2.connect(database="postgres", user="postgres", password="YOUR_PASSWORD_HERE", host="localhost", port="5432")

#create database cannot run inside a transaction, so autocommit is switched on
conn.autocommit = True

#create a cursor/pointer
cur = conn.cursor()

#create the database, or print a message if it already exists
try:
    cur.execute("create database music_discovery;")
    print("Database music_discovery created.")
except psycopg2.errors.DuplicateDatabase:
    print("Database music_discovery already exists.")

#close the cursor and the connection to the postgres database
cur.close()
conn.close()

#connect to the new database (replace YOUR_PASSWORD_HERE with your own password)
conn = psycopg2.connect(database="music_discovery", user="postgres", password="YOUR_PASSWORD_HERE", host="localhost", port="5432")
cur = conn.cursor()

#open the file holding the sql code that creates the tables
with open('./sql/create_tables.sql') as sqlfile:
    sql = sqlfile.read()

    #execute the sql code
    cur.execute(sql)

    #close the sql file
    sqlfile.close()

#commit the sql code to the database
conn.commit()
print("Tables created.")

#close the cursor object in the database
cur.close()
#close the database connection.
conn.close()
