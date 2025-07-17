# Map Query App - Agent Architecture

## Overview

The Map Query App uses OpenAI's Assistant API to provide natural language to SQL translation. The system maintains conversation context through thread IDs and includes robust error handling and query validation.

## Components

### Assistant Configuration

The application uses a custom-trained OpenAI Assistant that:
- Understands PostgreSQL syntax and best practices
- Has knowledge of our database schema (query_logs table)
- Generates safe and efficient SQL queries
- Maintains conversation context through threads
- Validates query safety and prevents harmful operations

### Implementation Details

The agent system consists of:

#### 1. Assistant Client (`app/agents/assistant_client.py`)
- Handles OpenAI API integration
- Manages thread-based conversations
- Processes natural language to SQL translation
- Implements retry logic and timeout handling

#### 2. Agent Routes (`app/api/routes/agent.py`)
- Exposes the `/api/agent/query` endpoint
- Validates request payloads
- Handles SQL extraction and cleanup
- Returns formatted responses

#### 3. SQL Runner (`app/services/sql_runner.py`)
- Executes generated SQL safely
- Implements connection pooling
- Handles database errors
- Returns standardized responses

#### 4. Query Logging
- Tracks all executed queries
- Stores execution timestamps
- Enables query analysis and optimization

## Usage Example

```python
# Natural language query
response = await client.post("/api/agent/query", json={
    "message": "Show me all queries from the last hour",
    "thread_id": "optional-thread-id"
})

# Response format
{
    "result": [...],       # Query results
    "thread_id": "...",    # Conversation thread ID
    "sql": "..."          # Generated SQL query
}
```

## Security Considerations

1. SQL Injection Prevention
   - All generated SQL is validated
   - Parameterized queries when possible
   - Schema-aware query generation

2. Rate Limiting
   - OpenAI API request throttling
   - Database connection pooling
   - Request timeout handling

3. Error Handling
   - Graceful failure modes
   - Detailed error messages
   - Query validation before execution

## Future Enhancements

1. Query Optimization
   - Performance analysis of generated queries
   - Schema-aware optimization suggestions
   - Query plan analysis

2. Advanced Natural Language Features
   - Follow-up question handling
   - Query refinement suggestions
   - Context-aware responses

3. Security Improvements
   - Role-based access control
   - Query auditing
   - Resource usage monitoring
