import psycopg2
import psycopg2.extras
from app.core.config import get_settings

settings = get_settings()


def run_raw_sql(query: str) -> list[dict]:
    """Execute a raw SQL query and return results as dicts."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT,
        )
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            if cur.description:
                return cur.fetchall()
            conn.commit()
            return [{"status": "Query executed successfully"}]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        if conn:
            conn.close()
