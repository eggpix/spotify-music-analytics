SELECT 
    tracks.name AS track,
    albums.name AS album,
    recently_played.played_at AS time
FROM recently_played
LEFT JOIN tracks
    ON tracks.id = recently_played.track_id
LEFT JOIN albums
    ON albums.id = tracks.album_id
ORDER BY time DESC
LIMIT 50;
