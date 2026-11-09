#import functions from flask
from flask import render_template, request

#import the package to connect to postgreSQL
import psycopg2

#import app variable from app package
from app import app


def get_db_connection():
    #connect to the database using the settings in config.py
    return psycopg2.connect(database=app.config['DB_NAME'], user=app.config['DB_USER'],
                            password=app.config['DB_PASSWORD'], host=app.config['DB_HOST'],
                            port=app.config['DB_PORT'])


#create an association for the URL /
@app.route('/')
#create an association for the URL /index
@app.route('/index')
def index():
    #create the home page
    return render_template('index.html', title='Music Discovery Database')


#create an association for the URL /about
@app.route('/about')
def about():
    #create the about us page
    return render_template('about.html', title='About Us')


#create an association for the URL /search, the chosen genre and mood come from the web address (?genre=3&mood=2)
@app.route('/search')
def search():
    genre_id = request.args.get('genre', '')
    mood_id = request.args.get('mood', '')

    conn = get_db_connection()
    cur = conn.cursor()

    #get the genres and the moods to fill the two drop-down lists
    cur.execute("select genre_id, name from genre order by name")
    genres = cur.fetchall()
    cur.execute("select mood_id, name from mood order by name")
    moods = cur.fetchall()

    #the sql code that finds the songs, with all the moods of each song joined into one text
    sql = ("select s.title, s.artist_name, g.name, string_agg(m.name, ', ' order by m.name), "
           "s.release_date, s.spotify_popularity "
           "from song s "
           "join genre g on s.genre_id = g.genre_id "
           "left join song_mood sm on s.song_id = sm.song_id "
           "left join mood m on sm.mood_id = m.mood_id")

    #add a condition for each filter that was chosen, only numbers are accepted
    #(%s is used instead of joining strings because the value comes from the web address)
    conditions = []
    values = []
    selected_genre = None
    selected_mood = None
    if genre_id.isdigit():
        selected_genre = int(genre_id)
        conditions.append("s.genre_id = %s")
        values.append(selected_genre)
    if mood_id.isdigit():
        selected_mood = int(mood_id)
        conditions.append("s.song_id in (select song_id from song_mood where mood_id = %s)")
        values.append(selected_mood)

    if len(conditions) > 0:
        sql = sql + " where " + " and ".join(conditions)

    #most popular songs first
    sql = sql + " group by s.song_id, g.name order by s.spotify_popularity desc, s.title"

    cur.execute(sql, values)
    songs = cur.fetchall()

    #close the cursor object and the database connection
    cur.close()
    conn.close()

    return render_template('search.html', title='Search', genres=genres, moods=moods, songs=songs,
                           selected_genre=selected_genre, selected_mood=selected_mood)
