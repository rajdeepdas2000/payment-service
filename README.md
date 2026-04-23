# Payment Service

## 🔗 Live Demo

- API Docs: https://payment-service-u2p7.onrender.com/docs


A backend payment reconciliation service for a partner integrating with Setu.

**Architecture** 

Client (Postman / Script) 

↓ 

FastAPI Application (Render) 

↓ 

PostgreSQL Database (Render)

All filtering, sorting, and aggregation operations are executed at the database level to ensure scalability.

**Components**

- FastAPI (Python): Handles API routing, validation, and request processing.

- PostgreSQL (Render Hosted): Stores events, transactions, and merchants with optimized schema.

- Data Loader Script (scripts/load_data.py): Simulates high-volume event ingestion (~10k+ events).

**Key Design Decisions**
- SQL is used for aggregation (GROUP BY), reconciliation queries, filtering
- Avoided Python-side processing for scalability
- Stateless API layer

## Setup Instructions (Local Development)

**Note**: `.env` file is not included. Please refer to `.env.example` and create `.env` file with appropriate database credentials.


1. Clone repository 
    
    
    `git clone https://github.com/rajdeepdas2000/payment-service.git`

    `cd payment-service`

2. Create virtual environment (Windows)
    
    
    `python -m venv venv`
    
    `venv\Scripts\activate`   

3. Install dependencies
    
    `pip install -r requirements.txt`

4. Setup PostgreSQL

    Ensure PostgreSQL is running locally.

    Create DB:

    `CREATE DATABASE payment_db;`

5. Configure environment variables

    Create .env:

    `DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/payment_db`

6. Run application
    
    `uvicorn app.main:app --reload`

7. Access API
    
    `http://127.0.0.1:8000/docs`

8. Load sample data
    
    `python scripts/load_data.py`

**API Documentation**

Base URL (Deployed)

    https://payment-service-u2p7.onrender.com

### POST /events

Ingests a payment event.

Example request
```json
{
  "event_id": "demo_1",
  "event_type": "payment_processed",
  "transaction_id": "txn_demo_1",
  "merchant_id": "merchant_1",
  "merchant_name": "FreshBasket",
  "amount": 1000,
  "currency": "INR",
  "timestamp": "2026-01-08T12:11:58"
}
```

Behavior
- Idempotent (duplicate event_id ignored)
- Updates transaction state

### GET /transactions

Returns all transactions

### GET /transactions/{txn_id}

Returns specific transaction

### GET /reconciliation/summary

Aggregated transaction summary:

- grouped by merchant, date, status

### GET /reconciliation/discrepancies

Finds inconsistent transactions:
- processed but not settled
- failed but settled


## Deployment Details
Platform: Render

Backend: FastAPI (Python 3)

Database: Render PostgreSQL

**Deployment Steps**

To load data into deployed service, update the URL in `scripts/load_data.py` to the Render endpoint.

1. Push code to GitHub

2. Create Web Service on Render

3. Set Start Command:

    `uvicorn app.main:app --host 0.0.0.0 --port 10000`

4. Add environment variable:
    
    `DATABASE_URL=<render-db-url>`

5. Access Live API

    https://payment-service-u2p7.onrender.com/docs


### Testing

- Postman collection included in GitHub repo

- Curl and browser testing used

- Large dataset (~10k events) tested

- Verified via:
    - API responses
    - direct SQL queries


**Idempotency Handling**

Handled using:

- Unique constraint on `event_id`

- Duplicate events are ignored safely

Ensures:

- No duplicate transaction updates

- Safe reprocessing of events

### Database Design

**Tables**
```
events
transactions
merchants
```

**Highlights**

- Primary keys (`transaction_id`, `event_id`) are indexed automatically
- Additional indexes added for filtering, subqueries and reconciliation queries on:
  - `merchant_id` 
  - `status` 
  - `events.transaction_id` 
- Aggregations done in SQL


### Assumptions and Tradeoffs
**Assumptions**

- Events arrive in near real-time

- Event ordering may not be guaranteed

- Transaction state derived from events

**Tradeoffs**

- No message queue
- No async processing (synchronous ingestion)
- Pagination implemented using offset/limit; cursor-based pagination would be more efficient for very large datasets/scalability
- Limited validation on currency/amount formats


**What could be improved**

- Add Kafka / queue for scalability
- Add caching (Redis)
- Add authentication
- Add retry mechanism for failed ingestion

### 🔗[Demo](https://drive.google.com/file/d/1EGC6lwcVS2IVU3STDXshAhTR3fx9MSN_/view?usp=sharing)

### Postman Collection

Included in repository:     **Payment Service.postman_collection.json**