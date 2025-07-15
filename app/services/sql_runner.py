import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


def run_raw_sql(query: str) -> list[dict]:
    """Execute a raw SQL query and return results as dicts."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432),
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
