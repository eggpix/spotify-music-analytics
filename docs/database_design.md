# Spotify Liked Songs Database Design

## Purpose

This database is designed to store a Spotify user's liked songs, as well as their relevant track information

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
- A track must belong to one or more artists.
- An artist may be associated with zero or more tracks.
- An album must belong to one or more artists.
- An artist may be associated with zero or more albums.
- An album must contain one or more tracks.
- A track must belong to exactly one album.