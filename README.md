# API Monitor System

**A high-performance, asynchronous API logging and monitoring architecture built with FastAPI/Python.**

> **Philosophy**: "Observability should never be the bottleneck."

This project demonstrates a production-grade monitoring pipeline that ingests, stores, aggregates, and summarizes API traffic without impacting the latency of the main application.

---

## 🏗️ Architecture & Decisions

### 1. Ingestion Strategy: "Zero-Overhead"
**Why Middleware + Background Tasks?**
We intercept requests using `LoggingMiddleware`, but we **never** write to the database in the request loop.
- **Problem**: Synchronous logging waits for disk I/O. If the DB slows down, the *user experience* degrades.
- **Solution**: We calculate latency, then hand off the data payload to a `clean_background_task`. The user gets their response immediately. The log is written asynchronously.

### 2. Database Design: "Read-Optimized"
**Why Composite Indices?**
We use composite indices like `(timestamp, status_code)`.
- **Reason**: Operators query logs by time range AND failure type (e.g., "Show me 500 errors from the last hour"). Scanning millions of rows linearly is unacceptable. These indices make forensics instant.

### 3. Aggregation: "Pre-computation"
**Why Background Jobs?**
We have a dedicated aggregation service that runs periodically (e.g., hourly).
- **Reason**: Calculating "Average Latency" across 1,000,000 rows on every dashboard refresh is expensive. We compute it *once*, store the summary, and serve the dashboard from that lightweight summary table.

### 4. AI Integration: "Summarization, Not Detection"
**Why is AI optional and constrained?**
We use AI (OpenAI/Gemini) to *explain* incidents, not to *detect* them.
- **Rule**: Mathematical thresholds (e.g., "Error rate > 5%") detect failure. AI reads the stack traces and summarizes the *meaning* (e.g., "Database connection timeout in user service").
- **Safety**: We never let AI decide severity or suppress logs. It is a "Co-pilot", not a "Pilot".

---

## ⚡ Quick Start

### 1. Prerequisites
*   Python 3.10+
*   PostgreSQL

### 2. Installation
```bash
git clone https://github.com/shriramrajat/API-Monitering-System.git
cd API-Monitering-System
python -m venv venv
# Activate venv
pip install -r requirements.txt
```

### 3. Configuration (.env)
```ini
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db_name
OPENAI_API_KEY=sk-... (Optional)
```

### 4. Run
```bash
# Start Server (Auto-reloads)
python -m uvicorn app.main:app --reload

# Access Dashboard
http://127.0.0.1:8000/dashboard
```

---

## 📂 Project Structure

```
├── app/
│   ├── main.py            # App entry point
│   ├── middleware.py      # The "Wire Tap" (Async Logger)
│   ├── models.py          # SQL Tables & Indices
│   ├── routers/
│   │   └── analytics.py   # Analysis API Endpoints
│   ├── services/
│   │   ├── log_service.py # Ingestion & Truncation Logic
│   │   ├── ai_service.py  # LLM Integration
│   │   └── aggregation_service.py # Background Worker logic
│   └── static/            # Minimal Dashboard UI
└── LOGGING_STRATEGY.md    # Deeper design notes
```

## 🛡️ Resilience Features
*   **Error Truncation**: Massive stack traces are chopped at 1000 chars to prevent DB flooding.
*   **UTC Enforcement**: All timestamps are normalized to prevent timezone drift.
*   **Batching Ready**: Architecture supports decoupling via message queues (if traffic scaled to millions/sec).

---
*Built with ❤️ for educational purposes.*
