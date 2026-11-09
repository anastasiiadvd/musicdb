-- Music Discovery Database: tables, relationships and fields
-- Note: the table for users is called "users" because "user" is a reserved word in PostgreSQL.

-- genre: lookup table of music genres
create table if not exists genre (
    genre_id serial primary key,
    name varchar(50) not null unique
);

-- mood: lookup table of mood tags
create table if not exists mood (
    mood_id serial primary key,
    name varchar(50) not null unique
);

-- users: registered users (passwords are stored hashed, never as plain text)
create table if not exists users (
    user_id serial primary key,
    username varchar(50) not null unique,
    email varchar(100) not null unique,
    password_hash varchar(255) not null,
    role varchar(20) not null default 'user' check (role in ('user', 'admin')),
    created_at timestamp not null default current_timestamp
);

-- song: main table, each song has one genre
create table if not exists song (
    song_id serial primary key,
    title varchar(150) not null,
    artist_name varchar(100) not null,
    album_name varchar(150),
    release_date date,
    spotify_streams bigint,
    spotify_popularity int,
    explicit boolean not null default false,
    genre_id int references genre(genre_id),
    unique (title, artist_name)
);

-- song_mood: many-to-many link between songs and moods
create table if not exists song_mood (
    song_id int not null references song(song_id) on delete cascade,
    mood_id int not null references mood(mood_id) on delete cascade,
    primary key (song_id, mood_id)
);

-- favourites: many-to-many link between users and their favourite songs
create table if not exists favourites (
    user_id int not null references users(user_id) on delete cascade,
    song_id int not null references song(song_id) on delete cascade,
    added_at timestamp not null default current_timestamp,
    primary key (user_id, song_id)
);
