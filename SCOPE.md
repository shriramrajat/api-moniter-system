# PROJECT SCOPE: API Log & Monitoring Service

## 1. What We WILL Build
- **API Request Logging**: Ingestion of timestamp, method, endpoint, status_code, latency_ms, error_message.
- **Queryable Logs**: Efficient storage and filtering (PostgreSQL).
- **Aggregated Summaries**: Error rates and latency stats calculated via background jobs.
- **(Later) AI Incident Summaries**: Generative AI for summarizing error patterns.

## 2. What We will NOT Build (Out of Scope)
- ❌ Distributed tracing
- ❌ Alerting engines
- ❌ Real-time dashboards (Standard dashboards only)
- ❌ Multi-service correlation

## 3. Core Philosophy
- **"What is breaking, where, how often, and why?"**
- If the system cannot answer this in seconds, it has failed.
- Focus on: Latency, Failure modes, Post-mortems, Operational visibility.
- **NO PII**. **NO Request Bodies**.
