SELECT tracks.name
FROM recently_played
LEFT JOIN tracks
    ON tracks.id = recently_played.track_id
ORDER BY recently_played.played_at DESC
LIMIT 10;
