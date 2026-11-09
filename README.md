# Music Discovery Database

**Student:** Anastasiia Davydchuk (R00250753)
**Module:** INFO8021 DevOps Strategy and Automation

A Flask web application connected to a PostgreSQL database that lets users search a music
database by genre and mood. Target audience: music listeners aged 16-35 (students, gym-goers,
commuters and casual listeners).

## Features
1. Search for music by genre
2. Register
3. Login
4. Filter music by mood
5. Add a song to favourites
6. Display a graph of song frequency by genre

## Technologies
Python / Flask, Flask-WTF, PostgreSQL, psycopg2, Werkzeug,
Git / GitHub, Docker, YAML pipeline, Visual Studio Code. Planned versions are in `tech-spec.yml`;
installed package versions are in `requirements.txt`.

## Branches
- `main` - initial website (Home and About Us pages, no functionality)
- `feature/login` - register (sign up), login and logout (uses the `users` table)
- `feature/search` - search by genre and mood (uses the `song`, `genre`, `mood` and `song_mood` tables)

The feature branches are intentionally not merged into `main`.

## Setup
1. Create and activate a virtual environment, then install the packages:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Open `initialise_db.py`, `populate_db.py` and `config.py` and replace `YOUR_PASSWORD_HERE` with your
   own PostgreSQL password.
3. Create the database and tables, then load the data:
   ```
   python initialise_db.py
   python populate_db.py
   ```
   Run `populate_db.py` once on empty tables. To start again, delete the tables in pgAdmin
   (music_discovery > Schemas > public > Tables, right-click, Drop (Force)), then run both scripts again.
4. Run the website and open http://127.0.0.1:5000
   ```
   python run.py
   ```

## Project structure
```
music_discovery/
  run.py                  starts the website
  config.py               Flask and database settings
  initialise_db.py        creates the database and tables
  populate_db.py          loads the CSV files into the tables
  requirements.txt
  tech-spec.yml
  sql/create_tables.sql
  data/                   one csv file per table, plus genre_mood_tags.csv
  app/
    __init__.py  routes.py
    static/stylesheet.css
    templates/    base.html  index.html  about.html
  extras/                 optional: prepare_data.py and the raw Kaggle file
```

## Data sources
- **Songs:** Kaggle "Most Streamed Spotify Songs 2024" (4,600 rows). Cleaned and reduced to the top
  100 songs (rules are in the report; `extras/prepare_data.py` applies them).
- **Genre and mood tags:** not in the Kaggle file. Assigned with GenAI assistance
  (`data/genre_mood_tags.csv`), then split into `genre.csv`, `mood.csv` and `song_mood.csv`.
- **Users and favourites:** 21 fictional demo users and 59 favourites generated with GenAI
  (`data/users.csv`, `data/favourites.csv`). Passwords are demo values only and are hashed on load.
