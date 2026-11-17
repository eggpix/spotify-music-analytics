SELECT artists.name
FROM recently_played
JOIN track_artists
    ON track_artists.track_id = recently_played.track_id
JOIN artists
    ON artists.id = track_artists.artist_id
GROUP BY artists.id, artists.name
ORDER BY MAX(recently_played.played_at) DESC
LIMIT 10;
