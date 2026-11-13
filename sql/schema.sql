-- CREATE TABLE queries for liked songs database

CREATE TABLE artists (
    artist_id VARCHAR(22) PRIMARY KEY,
    artist_name TEXT NOT NULL
);

CREATE TABLE albums (
	album_id VARCHAR(22) PRIMARY KEY,
	album_name TEXT NOT NULL,
	album_type VARCHAR(20) NOT NULL
);

CREATE TABLE tracks (
	track_id VARCHAR(22) PRIMARY KEY,
	track_name TEXT NOT NULL,
	track_duration INTEGER NOT NULL,
	album_id VARCHAR(22) NOT NULL REFERENCES albums(album_id)
);

CREATE TABLE track_artists (
    track_id VARCHAR(22) REFERENCES tracks(track_id),
    artist_id VARCHAR(22) REFERENCES artists(artist_id),
    artist_role VARCHAR(30),

    PRIMARY KEY (track_id, artist_id)
);

CREATE TABLE album_artists (
	album_id VARCHAR(22) REFERENCES albums(album_id),
	artist_id VARCHAR(22) REFERENCES artists(artist_id),
	artist_role VARCHAR(30),

	PRIMARY KEY (album_id, artist_id)
);