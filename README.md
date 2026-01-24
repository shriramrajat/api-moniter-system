# API Monitor System

**A high-performance, asynchronous API logging and monitoring architecture built with FastAPI.**

This project demonstrates how to build a production-grade monitoring service that ingests, stores, and analyzes API traffic without impacting application performance.

## 🚀 Key Features

*   **Zero-Overhead Logging**: Uses **Middleware + Background Tasks** to capture logs asynchronously. The user *never* waits for the database write.
*   **Granular Telemetry**: Captures **exact latency (ms)**, HTTP methods, endpoints, status codes, and full error traces.
*   **Failure Forensics**: Automtically catches unhandled exceptions (500s) and securely stores the stack trace for querying.
*   **Optimized Storage**: PostgreSQL schema optimized with compound indices for time-series querying.

## 🛠️ Tech Stack

*   **Core**: Python 3.13+, FastAPI
*   **Database**: PostgreSQL (with `asyncpg` driver), SQLAlchemy (Async ORM)
*   **Server**: Uvicorn (ASGI)

## ⚡ Quick Start

### 1. Prerequisites
*   Python 3.10+
*   PostgreSQL installed locally.

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/shriramrajat/API-Monitering-System.git
cd API-Monitering-System

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:

```ini
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost/YOUR_DB_NAME
```

### 4. Run the Server
```bash
python -m uvicorn app.main:app --reload
```
API will be live at `http://127.0.0.1:8000`.

## 📂 Project Structure

```
├── app/
│   ├── main.py            # Application entry point
│   ├── middleware.py      # The interceptor (captures requests)
│   ├── models.py          # Database tables (APILog, LogSummary)
│   ├── database.py        # Async DB connection logic
│   └── services/
│       └── log_service.py # Database write logic (Ingestion)
├── LOGGING_STRATEGY.md    # Detailed architecture decisions
├── SCHEMA.md              # Database schema documentation
└── requirements.txt
```

## 🔮 Roadmap
- [x] **Ingestion**: Core logging middleware.
- [ ] **Aggregation**: Background job to calculate hourly stats (Avg Latency, Error Rates).
- [ ] **Query API**: Endpoints to filter and view logs.
- [ ] **Dashboard**: Simple frontend to visualize the health of the system.
