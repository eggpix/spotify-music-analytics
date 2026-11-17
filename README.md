# Spotify Music Analytics

Spotify Music Analytics imports your saved tracks, listening history, and Spotify top tracks and artists into PostgreSQL. You can then use SQL to explore your music data with the included [example queries](docs/example_queries.md).

## Requirements

- Python and pip
- A PostgreSQL database, either on your computer or hosted remotely
- A Spotify developer app with the Spotify Web API enabled

Install the Python dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

## Configure Spotify access

Create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard). Set its redirect URI to `http://127.0.0.1:8888/callback`.

Create a `.env` file in the repository root with your app credentials:

```dotenv
SPOTIPY_CLIENT_ID="your_client_id_here"
SPOTIPY_CLIENT_SECRET="your_client_secret_here"
SPOTIPY_REDIRECT_URI="http://127.0.0.1:8888/callback"
```

Keep your client secret private. Do not commit `.env` or share its contents.

## Choose a PostgreSQL database

The importer connects to one PostgreSQL database per run. It does not copy data between a local and remote database or keep them synchronized; choose the destination by configuring the connection below.

### Local database

With `DATABASE_URL` unset, the importer connects to a local PostgreSQL server. By default it uses host `localhost`, port `5432`, database `spotify_music_analytics`, and user `postgres`. You can override these defaults in `.env`:

```dotenv
PGHOST="localhost"
PGPORT="5432"
PGDATABASE="spotify_music_analytics"
PGUSER="postgres"
PGPASSWORD="your_local_postgres_password"
```

Create the `spotify_music_analytics` database in PostgreSQL, then initialize its tables by running [sql/schema.sql](sql/schema.sql) against that database.

### Remote database

To use a hosted PostgreSQL database instead, set `DATABASE_URL` in `.env` to the connection URL supplied by your database provider:

```dotenv
DATABASE_URL="your_connection_url_here"
```

When `DATABASE_URL` is set, it takes precedence over all `PG*` settings and directs the importer to the remote database. Create the database if your provider requires it, then run [sql/schema.sql](sql/schema.sql) against that remote database before importing. Treat the connection URL as a secret, especially if it contains a password.

For either destination, the schema is the same. See [docs/database_design.md](docs/database_design.md) for the tables and their relationships.

## Import Spotify data

Run commands from the repository root:

```bash
python src/main.py
```

This updates recently played tracks. The importer checks the latest saved play time and requests newer plays, with a small overlap to avoid missing events at the boundary. Repeated records are ignored by the database's conflict handling.

For a fuller initial import, run:

```bash
python src/main.py --full
```

This imports saved (liked) tracks, snapshots of your top tracks and artists for Spotify's short-, medium-, and long-term ranges, and recently played tracks. The top-track and top-artist snapshots include their retrieval time and rank. The normal run does not refresh saved tracks or top lists; use `--full` when you want to collect those again.

## Query your data

Connect a PostgreSQL client, such as pgAdmin, to the same database you configured for the importer and run one of the [example queries](docs/example_queries.md).
