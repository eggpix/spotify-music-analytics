SELECT
    artists.name,
    COUNT(*) AS liked_count
FROM liked_tracks
JOIN track_artists
    ON track_artists.track_id = liked_tracks.track_id
JOIN artists
    ON artists.id = track_artists.artist_id
GROUP BY artists.id, artists.name
ORDER BY liked_count DESC
LIMIT 10;
