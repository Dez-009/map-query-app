"""Seed script for populating the database with sample query logs."""
import os
import sys
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import DictCursor

# Sample queries that might be logged in the application
SAMPLE_QUERIES = [
    "SELECT version()",
    "SELECT current_database()",
    "SELECT pg_size_pretty(pg_database_size(current_database()))",
    "SELECT count(*) FROM query_logs",
    "SELECT * FROM query_logs ORDER BY executed_at DESC LIMIT 5",
    "SELECT DATE_TRUNC('hour', executed_at) as hour, COUNT(*) FROM query_logs GROUP BY hour",
    "SELECT sql, COUNT(*) as frequency FROM query_logs GROUP BY sql ORDER BY frequency DESC",
    "SELECT * FROM query_logs WHERE sql LIKE '%SELECT%'",
    "SELECT * FROM query_logs WHERE sql LIKE '%INSERT%'",
    "SELECT * FROM query_logs WHERE sql LIKE '%UPDATE%'",
    "SELECT * FROM pg_stat_activity",
    "SELECT schemaname, tablename, n_live_tup FROM pg_stat_user_tables",
    "EXPLAIN ANALYZE SELECT * FROM query_logs",
    "SELECT pg_size_pretty(pg_total_relation_size('query_logs'))",
    "SELECT * FROM query_logs WHERE executed_at >= NOW() - INTERVAL '1 day'",
    "SELECT COUNT(*) FILTER (WHERE sql LIKE '%SELECT%') as selects, COUNT(*) FILTER (WHERE sql LIKE '%INSERT%') as inserts FROM query_logs",
    "SELECT * FROM query_logs WHERE sql ~* 'GROUP BY|ORDER BY|HAVING|JOIN'",
    "SELECT DATE_TRUNC('minute', executed_at) as minute, COUNT(*) FROM query_logs GROUP BY minute ORDER BY minute DESC",
    "SELECT * FROM query_logs WHERE LENGTH(sql) > 100",
    "SELECT sql, executed_at FROM query_logs ORDER BY LENGTH(sql) DESC LIMIT 5"
]

def main():
    """Insert sample data into the database."""
    print("Connecting to database...")
    conn = psycopg2.connect(
        host="db",
        database="mapquery",
        user="postgres",
        password="postgres",
        port=5432
    )
    print("Connected successfully!")
    
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            # Clear existing data
            cur.execute("TRUNCATE query_logs")
            
            # Insert sample queries with different timestamps
            base_time = datetime.now() - timedelta(days=1)
            for i, query in enumerate(SAMPLE_QUERIES):
                # Spread the queries over the last 24 hours
                executed_at = base_time + timedelta(minutes=i*72)  # 72 minutes = 1.2 hours between queries
                cur.execute(
                    "INSERT INTO query_logs (sql, executed_at) VALUES (%s, %s)",
                    (query, executed_at)
                )
            
            conn.commit()
            print("Successfully inserted sample data!")
            
            # Verify the data
            cur.execute("SELECT COUNT(*) FROM query_logs")
            count = cur.fetchone()[0]
            print(f"Total records in query_logs: {count}")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
