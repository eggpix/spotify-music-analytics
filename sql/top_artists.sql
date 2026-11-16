SELECT artists.name FROM top_artists
LEFT JOIN artists
    ON top_artists.artist_id = artists.id
WHERE top_artists.time_range = 'long_term'
AND top_artists.retrieved_at = (
    SELECT MAX(retrieved_at)
    FROM top_artists
    WHERE time_range = 'long_term'
)
ORDER BY top_artists.rank;
