import psycopg2
import psycopg2.extras
from app.core.config import get_settings

settings = get_settings()


def run_raw_sql(query: str) -> list[dict]:
    """Execute a raw SQL query and return results as dicts."""
    conn = None
    try:
        conn = psycopg2.connect(settings.get_db_url())
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            conn.commit()  # Commit for all queries
            if cur.description:
                return cur.fetchall()
            return [{"status": "Query executed successfully"}]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        if conn:
            conn.close()
