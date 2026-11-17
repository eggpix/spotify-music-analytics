-- spotify_music_analytics Database Schema
-- Run these queries to initialize the requied tables for the database

CREATE TABLE IF NOT EXISTS artists (
    id VARCHAR(22) PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
    id VARCHAR(22) PRIMARY KEY,
    name TEXT NOT NULL,
    type VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS tracks (
    id VARCHAR(22) PRIMARY KEY,
    name TEXT NOT NULL,
    duration_ms INTEGER NOT NULL,
    album_id VARCHAR(22) NOT NULL REFERENCES albums(id)
);

CREATE TABLE IF NOT EXISTS track_artists (
    track_id VARCHAR(22) REFERENCES tracks(id),
    artist_id VARCHAR(22) REFERENCES artists(id),
    artist_role VARCHAR(30),

    PRIMARY KEY (track_id, artist_id)
);

CREATE TABLE IF NOT EXISTS album_artists (
    album_id VARCHAR(22) REFERENCES albums(id),
    artist_id VARCHAR(22) REFERENCES artists(id),
    artist_role VARCHAR(30),

    PRIMARY KEY (album_id, artist_id)
);

CREATE TABLE IF NOT EXISTS liked_tracks (
    track_id VARCHAR(22) PRIMARY KEY REFERENCES tracks(id),
    liked_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS recently_played (
    track_id VARCHAR(22) REFERENCES tracks(id),
    played_at TIMESTAMPTZ NOT NULL,

    PRIMARY KEY (track_id, played_at)
);

CREATE TABLE IF NOT EXISTS top_tracks (
    track_id VARCHAR(22) REFERENCES tracks(id),
    time_range VARCHAR(20) NOT NULL
        CHECK (time_range IN ('short_term', 'medium_term', 'long_term')),
    retrieved_at TIMESTAMPTZ NOT NULL,
    rank INTEGER NOT NULL,

    PRIMARY KEY (track_id, time_range, retrieved_at)
);

CREATE TABLE IF NOT EXISTS top_artists (
    artist_id VARCHAR(22) REFERENCES artists(id),
    time_range VARCHAR(20) NOT NULL
        CHECK (time_range IN ('short_term', 'medium_term', 'long_term')),
    retrieved_at TIMESTAMPTZ NOT NULL,
    rank INTEGER NOT NULL,

    PRIMARY KEY (artist_id, time_range, retrieved_at)
);
