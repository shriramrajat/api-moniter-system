# TECHNOLOGY STACK

## Core Backend
- **Framework**: **FastAPI** (Python)
  - *Why*: High performance, native async support, perfect for handling high-throughput log ingestion.
- **Database**: **PostgreSQL**
  - *Why*: Robust, handles complex queries efficiently, supports powerful indexing for logs.
- **ORM**: **SQLAlchemy** (Async)
  - *Why*: Type-safe database interactions, mature ecosystem.
- **Background Tasks**: **FastAPI BackgroundTasks** (Start simple) / **Celery** (Scale)
  - *Why*: To offload aggregation and heavy lifting from the request/response cycle.

## Key Architectual Concepts to Demonstrate
1. **Middleware**
   - The heart of this project. We will capture requests *before* they hit the endpoint logic and logs *after* the response is generated.
2. **Indexing**
   - Critical for query performance. We will explicitly design indexes for `timestamp`, `status_code`, and `endpoint`.
3. **Aggregation**
   - Raw logs are for debugging; Aggregates are for insights. We will compute hourly/daily summaries.
4. **Read vs Write Optimization**
   - Logs are write-heavy. Analytics are read-heavy. Effectively balancing these is the goal.
