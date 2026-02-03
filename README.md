# API Monitor System

![API Monitor Banner](media/banner.png)

<div align="center">

**Next-Gen Asynchronous API Observability & Analytics Platform**

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](LICENSE)

</div>

---

## 📖 Overview

**API Monitor System** is a production-grade, high-performance monitoring architecture designed to provide deep observability into API traffic **without compromising latency**.

Unlike traditional synchronous logging which can slow down request processing, this system employs a **"Fire-and-Forget"** middleware strategy, offloading ingestion, analysis, and aggregation to background workers. It features a complete analytics dashboard with real-time charts, detailed logs, and **AI-powered incident reporting**.

### 🌟 Key Features

*   **🚀 Zero-Latency Logging**: Async middleware captures traffic without blocking the main thread.
*   **📊 Premium Dashboard**: Interactive charts for Latency Trends and Error Distribution (powered by Chart.js).
*   **🤖 AI Incident Reports**: Integrated with OpenAI/Gemini to automatically explain *why* errors are happening.
*   **🛡️ Rate Limiting**: Token-bucket algorithm protection against abuse and DDoS attempts.
*   **💾 Optimized Storage**: PostgreSQL with composite indices for instant querying of millions of logs.
*   **⚡ Auto-Aggregation**: Background jobs pre-calculate hourly statistics for instant dashboard loading.
*   **🐳 Dockerized**: "One-click" deployment with Docker Compose.

---

## 🏗️ Architecture

The system follows a decoupled, event-driven design to ensure resilience and speed.

```mermaid
graph TD
    User([User Request]) -->|HTTP| Middleware[🛡️ Middleware & Rate Limiter]
    Middleware -->|Pass| API[FastAPI Handler]
    API -->|Response| User
    
    Middleware -.->|Async Log| Background[Background Task]
    Background -->|Insert| DB[(PostgreSQL)]
    
    Scheduler[⏰ Hourly Scheduler] -->|Trigger| Aggregator[Aggregation Service]
    Aggregator -->|Read Raw Logs| DB
    Aggregator -->|Write Summary| DB
    
    Dashboard([🖥️ Dashboard]) -->|Read Summary| DB
    Dashboard -->|AI Query| AI[🤖 OpenAI/Gemini]
```

---

## 🛠️ Tech Stack

*   **Backend Framework**: FastAPI (Python)
*   **Database**: PostgreSQL (AsyncPG + SQLAlchemy 2.0)
*   **Migrations**: Alembic
*   **Resilience**: Rate Limiting (Token Bucket), Retries
*   **Frontend**: HTML5, Vanilla JS, Chart.js
*   **Scheduling**: APScheduler
*   **Deployment**: Docker & Docker Compose

---

## 🚀 Quick Start

### Option A: Docker (Recommended)

Run the entire stack (App + DB) with a single command:

```bash
docker-compose up --build
```
Access the dashboard at `http://localhost:8001/dashboard`.

### Option B: Local Development

**1. Clone the Repository**
```bash
git clone https://github.com/shriramrajat/api-moniter-system.git
cd api-moniter-system
```

**2. Setup Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment**
Create a `.env` file (see `.env.example`):
```ini
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/api_moniter
OPENAI_API_KEY=your_key_here
```

**5. Initialize Database**
```bash
alembic upgrade head
```

**6. Run Server**
```bash
python -m uvicorn app.main:app --reload
```
Visit `http://127.0.0.1:8000/dashboard` to see your metrics!

---

## 📸 Screenshots

| **Live Dashboard** | **Incident Analysis** |
|:---:|:---:|
| <img src="media/01.png" alt="Dashboard" width="100%"> | <img src="media/02.png" alt="AI Analysis" width="100%"> |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <p>Built with ❤️ by <b>Rajat Shriram</b></p>
</div>
