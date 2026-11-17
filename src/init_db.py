"""
Initialize Database using schema file.
"""

from pathlib import Path
from database import connect

def main():
    schema_path = Path(__file__).parent.parent / "sql" / "schema.sql"
    schema = schema_path.read_text(encoding="utf-8")

    db = connect()

    try:
        with db.cursor() as cursor:
            cursor.execute(schema)
        db.commit()
        print("Database initialized successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()