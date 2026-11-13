# Spotify Liked Songs Database Design

## Purpose

This database is designed to store a Spotify user's liked songs, as well as their relevant track information

## Entities

| Entity      | Primary Key         |
| ----------- | ------------------- |
| Track       | Track ID            |
| Artist      | Artist ID           |
| Album       | Album ID            |
| TrackArtist | Track ID, Artist ID |
| AlbumArtist | Album ID, Artist ID |

## Attributes

- Track
  - Track ID - VARCHAR(22)
  - Track Name - TEXT
  - Track Duration - INTEGER
  - Album ID **(Foreign Key)**
- Album
  - Album ID - VARCHAR(22)
  - Album Name - TEXT
  - Album Type - VARCHAR(20) (Single, Album, or EP)
- Artist
  - Artist ID - VARCHAR(22)
  - Artist Name - TEXT
- TrackArtist
  - Track ID **(Foreign Key)**
  - Artist ID **(Foreign Key)**
  - Artist Role - VARCHAR(30) *(Primary, Featured, etc.)*
- AlbumArtist
  - Album ID **(Foreign Key)**
  - Artist ID **(Foreign Key)**
  - Artist Role - VARCHAR(30) *(Primary, Featured, etc.)*

## Relationships
- A track must belong to one or more artists.
- An artist may be associated with zero or more tracks.
- An album must belong to one or more artists.
- An artist may be associated with zero or more albums.
- An album must contain one or more tracks.
- A track must belong to exactly one album.