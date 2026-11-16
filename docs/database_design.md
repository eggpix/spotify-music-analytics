# Spotify Liked Songs Database Design

## Purpose

This database is designed to store a Spotify user's liked songs, as well as their relevant track information

## Entities

| Entity        | Primary Key         |
| ------------- | ------------------- |
| tracks        | track_id            |
| artists       | artist_id           |
| albums        | album_id            |
| track_artists | track_id, artist_id |
| album_artists | album_id, artist_id |

## Attributes

### tracks

| Field       | Type        | Key                 |
| ----------- | ----------- | ------------------- |
| id          | VARCHAR(22) | PK                  |
| name        | TEXT        |                     |
| duration    | INTEGER     |                     |
| album_id    | VARCHAR(22) | FK → albums.id      |

### albums

| Field       | Type        | Key                 |
| ----------- | ----------- | ------------------- |
| id          | VARCHAR(22) | PK                  |
| name        | TEXT        |                     |
| type        | VARCHAR(20) |                     |

### artists

| Field       | Type        | Key                 |
| ----------- | ----------- | ------------------- |
| id          | VARCHAR(22) | PK                  |
| name        | TEXT        |                     |

### track_artists

| Field       | Type        | Key                 |
| ----------- | ----------- | ------------------- |
| track_id    | VARCHAR(22) | PK, FK → tracks.id  |
| artist_id   | VARCHAR(22) | PK, FK → artists.id |
| artist_role | VARCHAR(30) |                     |

### album_artists

| Field       | Type        | Key                 |
| ----------- | ----------- | ------------------- |
| album_id    | VARCHAR(22) | PK, FK → albums.id  |
| artist_id   | VARCHAR(22) | PK, FK → artists.id |
| artist_role | VARCHAR(30) |                     |

## Relationships
- A track must belong to one or more artists.
- An artist may be associated with zero or more tracks.
- An album must belong to one or more artists.
- An artist may be associated with zero or more albums.
- An album must contain one or more tracks.
- A track must belong to exactly one album.