# FlowPilot AI

FlowPilot AI is an AI-powered customer support automation backend built with Python and FastAPI. It analyzes incoming customer requests using the Gemini API, extracts structured information, retrieves verified order data from a SQL database, applies business rules, generates customer-facing responses, and stores processed requests for later retrieval.

The project demonstrates practical integration of LLMs with REST APIs, structured outputs, SQL persistence, business logic, automated testing, and external API handling.

## Features

- AI-powered customer request classification
- Structured LLM output using Pydantic schemas
- Automatic extraction of order IDs from natural-language requests
- Order lookup using SQLite and SQL queries
- Rule-based action selection using verified order information
- AI-generated customer responses
- Persistent support-request history
- REST API built with FastAPI
- Automatic interactive API documentation with Swagger
- Retry handling for temporary Gemini API failures
- Environment-variable based API key management
- Automated tests with pytest
- Docker configuration included for future containerized deployment

## Architecture

```text
Customer Request
       |
       v
+---------------+
|    FastAPI    |
+-------+-------+
        |
        v
+-------------------+
| Gemini Classifier |
+---------+---------+
          |
          | Structured Output
          v
+-------------------+
|  Decision Engine  |
+---------+---------+
          |
          +--------------------+
          |                    |
          v                    v
+----------------+      +---------------+
| SQLite Orders  |      | Business Rules|
|    Database    |      +---------------+
+-------+--------+
        |
        +-----------+
                    |
                    v
          +------------------+
          | Gemini Responder |
          +--------+---------+
                   |
                   v
          Customer Response
                   |
                   v
          +-----------------+
          | Request History |
          |     SQLite      |
          +-----------------+
```

## Example Workflow

A customer sends:

```json
{
  "message": "My order 5832 was supposed to arrive yesterday but I still haven't received it."
}
```

FlowPilot:

1. Sends the message to Gemini for classification.
2. Extracts the request category, priority, order ID, and summary.
3. Looks up order `5832` in the SQLite database.
4. Uses business rules to determine the appropriate action.
5. Generates a customer-facing response using verified order information.
6. Stores the processed request and response in the database.

Example response:

```json
{
  "request_id": 1,
  "analysis": {
    "category": "delivery_issue",
    "priority": "medium",
    "order_id": "5832",
    "summary": "Order 5832 has not arrived as expected."
  },
  "order": {
    "order_id": "5832",
    "customer_name": "Alex Morgan",
    "status": "delayed",
    "expected_delivery": "2026-09-21",
    "current_location": "Munich Distribution Center"
  },
  "action": "inform_customer_about_delay",
  "customer_response": "Your order 5832 is currently delayed and is at the Munich Distribution Center."
}
```

The exact AI-generated text may vary between requests.

## Tech Stack

- Python 3.11
- FastAPI
- Gemini API
- Google GenAI Python SDK
- Pydantic
- SQLite
- SQL
- pytest
- Uvicorn
- python-dotenv
- Git & GitHub
- Docker configuration

## REST API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | API health check |
| GET | `/orders/{order_id}` | Retrieve an order from the database |
| GET | `/history` | Retrieve processed support requests |
| POST | `/analyze` | Analyze and process a customer request |

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Database

FlowPilot uses SQLite with two main tables.

### `orders`

Stores order information including:

- Order ID
- Customer name
- Order status
- Expected delivery date
- Current location

### `support_requests`

Stores processed requests including:

- Original customer message
- AI-generated category and priority
- Extracted order ID
- Request summary
- Selected action
- Generated customer response
- Processing timestamp

Parameterized SQL queries are used when reading and writing database records.

## Project Structure

```text
FlowPilot-AI/
|
|-- app/
|   |-- __init__.py
|   |-- classifier.py
|   |-- config.py
|   |-- database.py
|   |-- decision.py
|   |-- main.py
|   |-- models.py
|   |-- responder.py
|   `-- tools.py
|
|-- data/
|   `-- orders.json
|
|-- tests/
|   |-- __init__.py
|   `-- test_decision.py
|
|-- .dockerignore
|-- .gitignore
|-- Dockerfile
|-- README.md
`-- requirements.txt
```

The runtime SQLite database is excluded from Git.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kaspersky006/FlowPilot--AI.git
cd FlowPilot--AI
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git to prevent API credentials from being committed.

### 4. Start the API

```bash
python -m uvicorn app.main:app
```

Open:

```text
http://127.0.0.1:8000/docs
```

The database and initial sample orders are created automatically when the application starts.

## Testing

Run the automated tests with:

```bash
python -m pytest -v
```

Current tests validate important decision-engine behavior including:

- Delayed orders
- Missing orders
- Refund requests

The tests are intentionally independent of the Gemini API so they can run quickly without consuming API quota.

## Error Handling

Gemini requests include retry logic to handle temporary API failures such as service-unavailable responses.

The API also handles cases such as:

- Unknown order IDs
- Invalid history limits
- Empty AI responses
- Temporary AI service failures

## Security

API credentials are loaded through environment variables and are not stored in source code.

The `.env` file and runtime database are excluded through `.gitignore`.

## Docker

A Dockerfile and `.dockerignore` are included for containerization. Docker execution has not yet been validated in the current development environment.

## Future Improvements

Potential extensions include:

- PostgreSQL or MySQL migration
- n8n workflow integration
- Authentication and authorization
- Additional automated tests and API mocking
- Human-in-the-loop approval for sensitive actions
- RAG-based support knowledge retrieval
- Deployment to a cloud platform
- Monitoring and observability