# API Documentation

The API exposes endpoints for running raw SQL queries and checking service health. All responses are JSON.

## `GET /`

Returns a simple status message.

**Example**
```json
{"message": "Map Query API is up!"}
```

## `POST /api/query`

Execute a raw SQL statement against the connected PostgreSQL database.

### Request Body

```json
{
  "sql": "SELECT 1;"
}
```

### Response

- On success, returns a list of rows:
```json
{
  "result": [
    {"?column?": 1}
  ]
}
```
- On error, returns HTTP 400 with an error message.

### Notes

Use this endpoint with caution. It executes whatever SQL is provided. Future versions will route natural language to SQL via OpenAI agents.
