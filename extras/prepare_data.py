#OPTIONAL EXTRA (not required by the assignment).
#Cleans the raw Kaggle spreadsheet and writes the csv files that populate_db.py reads.
#Run from the project folder:  python extras/prepare_data.py
import csv
import datetime
import os
import re

#openpyxl reads the .xlsx file
import openpyxl

BASE = os.path.join(os.path.dirname(__file__), "..")
RAW_FILE = os.path.join(BASE, "extras", "Most_Streamed_Spotify_Songs_2024.xlsx")
TAGS_FILE = os.path.join(BASE, "data", "genre_mood_tags.csv")
DATA_DIR = os.path.join(BASE, "data")

SONG_COUNT = 100        #number of songs to keep
MIN_POPULARITY = 60     #quality filter: removes covers, ringtones and near-unheard tracks

#characters that show the text was corrupted in the original file (e.g. "Beyoncï¿")
CORRUPTED = re.compile("\ufffd|ï¿|ý|Ã|Â|ð")


def fix_date(value):
    #the file mixes two date formats. Ambiguous M/D/YYYY dates were turned into real dates
    #by reading them as D/M, so the month and day are swapped. Dates where the day is above 12
    #stayed as text in M/D/YYYY format and are already correct.
    if isinstance(value, datetime.datetime):
        return datetime.date(value.year, value.day, value.month)
    month, day, year = (int(part) for part in value.split("/"))
    return datetime.date(year, month, day)


def load_clean_songs():
    sheet = openpyxl.load_workbook(RAW_FILE, read_only=True).active
    rows = list(sheet.iter_rows(values_only=True))
    col = {name: i for i, name in enumerate(rows[0])}
    seen, songs = set(), []
    for row in rows[1:]:
        title, artist = row[col["Track"]], row[col["Artist"]]
        if title is None or artist is None:
            continue
        title, artist = str(title).strip(), str(artist).strip()
        album = str(row[col["Album Name"]] or "").strip()
        if CORRUPTED.search(title + artist + album):
            continue
        streams, popularity = row[col["Spotify Streams"]], row[col["Spotify Popularity"]]
        if streams is None or popularity is None or int(popularity) < MIN_POPULARITY:
            continue
        key = (title.lower(), artist.lower())
        if key in seen:
            continue
        seen.add(key)
        songs.append([title, artist, album, fix_date(row[col["Release Date"]]).isoformat(),
                      int(streams), int(popularity), "true" if int(row[col["Explicit Track"]]) == 1 else "false"])
    return songs


def write_csv(name, rows):
    #no header row, one csv file per table (the same layout as the class example)
    with open(os.path.join(DATA_DIR, name), "w", newline="", encoding="utf-8") as out:
        csv.writer(out).writerows(rows)


if __name__ == "__main__":
    songs = load_clean_songs()[:SONG_COUNT]

    #genre and mood are not in the Kaggle file, they come from data/genre_mood_tags.csv
    with open(TAGS_FILE, newline="", encoding="utf-8") as tagfile:
        tags = {(r["title"], r["artist_name"]): r for r in csv.DictReader(tagfile)}
    for s in songs:
        if (s[0], s[1]) not in tags:
            raise SystemExit("No genre/mood tags for: " + s[0])

    #ids are the row positions (1, 2, 3...) because the database numbers rows in insertion order
    genres = sorted({tags[(s[0], s[1])]["genre"] for s in songs})
    moods = sorted({m for s in songs for m in tags[(s[0], s[1])]["moods"].split(";")})
    write_csv("genre.csv", [[g] for g in genres])
    write_csv("mood.csv", [[m] for m in moods])
    write_csv("songs.csv", [s + [genres.index(tags[(s[0], s[1])]["genre"]) + 1] for s in songs])
    write_csv("song_mood.csv", [[i, moods.index(m) + 1] for i, s in enumerate(songs, 1)
                                for m in tags[(s[0], s[1])]["moods"].split(";")])
    print(str(len(songs)) + " songs written.")
