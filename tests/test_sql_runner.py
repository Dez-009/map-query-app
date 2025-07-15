from app.services.sql_runner import run_raw_sql


def test_run_raw_sql():
    create = run_raw_sql(
        "CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name TEXT);"
    )
    assert isinstance(create, list)

    insert = run_raw_sql("INSERT INTO test_table (name) VALUES ('Dez');")
    assert insert == [{"status": "Query executed successfully"}]

    select = run_raw_sql("SELECT * FROM test_table;")
    assert isinstance(select, list)
    assert select[0]["name"] == "Dez"

    drop = run_raw_sql("DROP TABLE test_table;")
    assert drop == [{"status": "Query executed successfully"}]
