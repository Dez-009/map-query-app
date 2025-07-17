# API Documentation

The API provides comprehensive property management capabilities and a natural language query interface. All responses are in JSON format.

## Overview

### Property Management Endpoints

- `/api/properties` - Property management
- `/api/units` - Unit operations
- `/api/residents` - Resident management
- `/api/payments` - Payment processing
- `/api/repairs` - Maintenance requests
- `/api/pets` - Pet registration
- `/api/vehicles` - Vehicle management

### Query Interface

- `/api/agent/query` - Natural language queries
- `/api/query` - Direct SQL execution

## Base Endpoint

### `GET /`

Returns the API status.

**Example Response:**
```json
{"message": "Map Query API is up!"}
```

## `POST /api/agent/query`

Translate natural language to SQL and execute the query. Uses OpenAI's Assistant API for intelligent SQL generation.

### Request Body
```json
{
  "message": "Show me all queries from the last hour",
  "thread_id": "optional-thread-id-for-conversation-context"
}
```

### Response
```json
{
  "result": [...],         // Query results as array of objects
  "thread_id": "...",     // OpenAI conversation thread ID
  "sql": "..."            // Generated SQL query
}
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

## Property Management

### Properties

#### `GET /api/properties`
List all properties.

#### `POST /api/properties`
Create a new property.
```json
{
  "name": "Sunset Apartments",
  "address": "123 Main St",
  "city": "Springfield",
  "state": "IL",
  "zip_code": "62701"
}
```

#### `GET /api/properties/{id}`
Get property details including units.

### Units

#### `GET /api/units`
List all units.

#### `POST /api/units`
Create a new unit.
```json
{
  "property_id": 1,
  "unit_number": "101",
  "bedrooms": 2,
  "bathrooms": 1,
  "square_feet": 850,
  "rent_amount": 1200.00
}
```

### Residents

#### `GET /api/residents`
List all residents.

#### `POST /api/residents`
Register a new resident.
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "555-0123",
  "unit_id": 1
}
```

### Payments

#### `GET /api/payments`
List all payments.

#### `POST /api/payments`
Record a new payment.
```json
{
  "resident_id": 1,
  "amount": 1200.00,
  "payment_type": "RENT",
  "payment_method": "CREDIT_CARD"
}
```

### Repairs

#### `GET /api/repairs`
List all repair requests.

#### `POST /api/repairs`
Submit a repair request.
```json
{
  "unit_id": 1,
  "description": "Leaking faucet",
  "priority": "MEDIUM",
  "status": "PENDING"
}
```

### Pets

#### `GET /api/pets`
List all registered pets.

#### `POST /api/pets`
Register a new pet.
```json
{
  "resident_id": 1,
  "name": "Buddy",
  "type": "DOG",
  "breed": "Golden Retriever"
}
```

### Vehicles

#### `GET /api/vehicles`
List all registered vehicles.

#### `POST /api/vehicles`
Register a new vehicle.
```json
{
  "resident_id": 1,
  "make": "Toyota",
  "model": "Camry",
  "year": 2020,
  "license_plate": "ABC123"
}
```
