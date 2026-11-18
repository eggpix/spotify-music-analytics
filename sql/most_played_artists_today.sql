SELECT artists.name AS artist,
COUNT(artists.id) AS times_played
FROM recently_played
LEFT JOIN tracks
    ON recently_played.track_id = tracks.id
LEFT JOIN track_artists
    ON track_artists.track_id = tracks.id
LEFT JOIN artists
    ON artists.id = track_artists.artist_id
WHERE recently_played.played_at >=
    date_trunc('day', CURRENT_TIMESTAMP AT TIME ZONE 'America/Phoenix')
    AT TIME ZONE 'America/Phoenix'
    AND recently_played.played_at <
    (date_trunc('day', CURRENT_TIMESTAMP AT TIME ZONE 'America/Phoenix')
    + INTERVAL '1 day')
    AT TIME ZONE 'America/Phoenix'
GROUP BY artists.id, artists.name
ORDER BY times_played DESC
LIMIT 10;
