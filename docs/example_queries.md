# Example Queries

## Top Artists

Retrieve the user's top artists (long term).

[View Query](../sql/top_artists.sql)

## Recently Played Tracks

Retrieve list of 50 recently played tracks. As of November 2026, Spotify appears to only log songs listened to completion, so keep that in mind when using this query.

[View Query](../sql/recently_played.sql)

## Most Liked Artists

Retrieve table of artists with most liked songs.

[View Query](../sql/most_liked_artists.sql)

## Most Played Artists Today

Retrieve table of most played artists on the current date. Replace `'America/Phoenix'` with your own timezone. Note that Spotify only returns a max of 50 recent tracks. It is recommended to get recent songs on a schedule if you hope to get a comprehensive list of songs played on a specific date.

[View Query](../sql/most_played_artists_today.sql)