#import packages to allow to open a csv file and a connection to postgreSQL database
import psycopg2
import csv

#import security to encrypt password before inserting in to table.
from werkzeug.security import generate_password_hash

#connect to the database (replace YOUR_PASSWORD_HERE with your own password)
conn = psycopg2.connect(database="music_discovery", user="postgres", password="YOUR_PASSWORD_HERE", host="localhost", port="5432")

#create a cursor/pointer
cur = conn.cursor()

#store the path of the csv files in a variable
path = './data/'

#The tables are empty, so the database numbers the rows 1, 2, 3... in the order they are inserted.
#The csv files that link tables together (songs.csv, song_mood.csv, favourites.csv) use these row numbers
#as ids, so the tables must be filled in this order: genre, mood, users, song, song_mood, favourites.

#open data file and read in data row by row to insert into table genre
with open(path + 'genre.csv', newline='') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=',')
    for row in dataReader:
        #create the sql code to insert the values into the table genre
        sql = "insert into genre (name) values ('" + row[0] + "');"

        #execute the sql code
        cur.execute(sql)

    #close the csv file
    csvfile.close()

#open data file and read in data row by row to insert into table mood
with open(path + 'mood.csv', newline='') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=',')
    for row in dataReader:
        #create the sql code to insert the values into the table mood
        sql = "insert into mood (name) values ('" + row[0] + "');"

        #execute the sql code
        cur.execute(sql)

    #close the csv file
    csvfile.close()

#open data file and read in data row by row to insert into table users
with open(path + 'users.csv', newline='') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=',')
    for row in dataReader:
        #create the sql code to insert the values into the table users, the password is hashed first
        sql = "insert into users (username, email, password_hash, role) values ('" + row[0] + "','" + row[1] + "','" + generate_password_hash(row[2]) + "','" + row[3] + "');"

        #execute the sql code
        cur.execute(sql)

    #close the csv file
    csvfile.close()

#open data file and read in data row by row to insert into table song
with open(path + 'songs.csv', newline='') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=',')
    for row in dataReader:
        #an apostrophe would end the sql text early, so each one is doubled (Livin' becomes Livin'')
        title = row[0].replace("'", "''")
        artist = row[1].replace("'", "''")
        album = row[2].replace("'", "''")

        #create the sql code to insert the values into the table song
        sql = "insert into song (title, artist_name, album_name, release_date, spotify_streams, spotify_popularity, explicit, genre_id) values ('" + title + "','" + artist + "','" + album + "','" + row[3] + "','" + row[4] + "','" + row[5] + "','" + row[6] + "','" + row[7] + "');"

        #execute the sql code
        cur.execute(sql)

    #close the csv file
    csvfile.close()

#open data file and read in data row by row to insert into table song_mood
with open(path + 'song_mood.csv', newline='') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=',')
    for row in dataReader:
        #create the sql code to insert the values into the table song_mood
        sql = "insert into song_mood (song_id, mood_id) values ('" + row[0] + "','" + row[1] + "');"

        #execute the sql code
        cur.execute(sql)

    #close the csv file
    csvfile.close()

#open data file and read in data row by row to insert into table favourites
with open(path + 'favourites.csv', newline='') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=',')
    for row in dataReader:
        #create the sql code to insert the values into the table favourites
        sql = "insert into favourites (user_id, song_id) values ('" + row[0] + "','" + row[1] + "');"

        #execute the sql code
        cur.execute(sql)

    #close the csv file
    csvfile.close()

#commit the sql code to the database
conn.commit()
#close the cursor object in the database
cur.close()
#close the database connection.
conn.close()
