# Spotify Music Analytics Database Design

## Purpose

This database is designed to store a Spotify user's liked songs, recently played songs, and top artists and tracks, as well as any relevant information such as album information.

## Entities

- tracks
- artists
- albums
- track_artists
- album_artists
- liked_tracks
- recently_played
- top_tracks
- top_artists

## Attributes

### tracks

| Field        | Type        | Key                 |
| ------------ | ----------- | ------------------- |
| id           | VARCHAR(22) | PK                  |
| name         | TEXT        |                     |
| duration_ms  | INTEGER     |                     |
| album_id     | VARCHAR(22) | FK → albums.id      |

### albums

| Field        | Type        | Key                 |
| ------------ | ----------- | ------------------- |
| id           | VARCHAR(22) | PK                  |
| name         | TEXT        |                     |
| type         | VARCHAR(20) |                     |

### artists

| Field        | Type        | Key                 |
| ------------ | ----------- | ------------------- |
| id           | VARCHAR(22) | PK                  |
| name         | TEXT        |                     |

### track_artists

| Field        | Type        | Key                 |
| ------------ | ----------- | ------------------- |
| track_id     | VARCHAR(22) | PK, FK → tracks.id  |
| artist_id    | VARCHAR(22) | PK, FK → artists.id |
| artist_role  | VARCHAR(30) |                     |

### album_artists

| Field        | Type        | Key                 |
| ------------ | ----------- | ------------------- |
| album_id     | VARCHAR(22) | PK, FK → albums.id  |
| artist_id    | VARCHAR(22) | PK, FK → artists.id |
| artist_role  | VARCHAR(30) |                     |

### liked_tracks
| Field        | Type        | Key                 |
| ------------ | ----------- | ------------------- |
| track_id     | VARCHAR(22) | PK FK → tracks.id   |
| liked_at     | TIMESTAMPTZ |                     |

### recently_played

| Field        | Type        | Key                 |
| ------------ | ----------- | ------------------- |
| track_id     | VARCHAR(22) | PK, FK → tracks.id  |
| played_at    | TIMESTAMPTZ | PK                  |

### top_tracks

| Field        | Type        | Key                 |
| ------------ | ----------- | ------------------- |
| track_id     | VARCHAR(22) | PK, FK → tracks.id  |
| time_range   | VARCHAR(20) | PK                  |
| retrieved_at | TIMESTAMPTZ | PK                  |
| rank         | INTEGER     |                     |

### top_artists

| Field        | Type        | Key                 |
| ------------ | ----------- | ------------------- |
| artist_id    | VARCHAR(22) | PK, FK → artists.id |
| time_range   | VARCHAR(20) | PK                  |
| retrieved_at | TIMESTAMPTZ | PK                  |
| rank         | INTEGER     |                     |

## Relationships

The data model uses junction tables to represent many-to-many relationships and to preserve artist roles.

- A track can be associated with zero or more artists through `track_artists`.
- An artist can be associated with zero or more tracks through `track_artists`.
- An album can be associated with zero or more artists through `album_artists`.
- An artist can be associated with zero or more albums through `album_artists`.
- An album can contain one or more tracks.
- Each track belongs to exactly one album via `tracks.album_id -> albums.id`.
- Each `track_artists` row links one track to one artist and records that artist's role for that track.
- Each `album_artists` row links one album to one artist and records that artist's role for that album.

In summary, the schema is:

- `tracks` to `albums`: many-to-one
- `tracks` to `artists`: many-to-many via `track_artists`
- `albums` to `artists`: many-to-many via `album_artists`