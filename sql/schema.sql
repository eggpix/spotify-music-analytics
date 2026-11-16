-- CREATE TABLE queries for liked songs database

CREATE TABLE artists (
    id VARCHAR(22) PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE albums (
	id VARCHAR(22) PRIMARY KEY,
	name TEXT NOT NULL,
	type VARCHAR(20) NOT NULL
);

CREATE TABLE tracks (
	id VARCHAR(22) PRIMARY KEY,
	name TEXT NOT NULL,
	duration_ms INTEGER NOT NULL,
	album_id VARCHAR(22) NOT NULL REFERENCES albums(id)
);

CREATE TABLE track_artists (
    track_id VARCHAR(22) REFERENCES tracks(id),
    artist_id VARCHAR(22) REFERENCES artists(id),
    artist_role VARCHAR(30),

    PRIMARY KEY (track_id, artist_id)
);

CREATE TABLE album_artists (
	album_id VARCHAR(22) REFERENCES albums(id),
	artist_id VARCHAR(22) REFERENCES artists(id),
	artist_role VARCHAR(30),

	PRIMARY KEY (album_id, artist_id)
);