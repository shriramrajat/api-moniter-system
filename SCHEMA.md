# DATABASE SCHEMA

## 1. Raw Logs Table: `api_logs`
*The raw truth of every request.*

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **id** | Integer | PK, Auto-increment | Unique identifier for each log entry. |
| **timestamp** | DateTime | Not Null | Exact time of the request. |
| **method** | String | Not Null | HTTP Method (GET, POST, etc.). |
| **endpoint** | String | Not Null | The resource path accessed. |
| **status_code** | Integer | Not Null | HTTP response code (200, 404, 500, etc.). |
| **latency_ms** | Float | Not Null | Time taken to process the request (in milliseconds). |
| **error_message** | String | Nullable | Captured error details, if any. |

### 🔍 Indexes (CRITICAL)
*Indexes are how adults handle specific read patterns on write-heavy tables.*
- `(timestamp)`: Optimized for time-range queries (e.g., "logs from last hour").
- `(status_code)`: Optimized for filtering by result (e.g., "show me all 500s").
- `(endpoint)`: Optimized for filtering by specific API routes.
- `(timestamp, status_code)`: Optimized for compound queries (e.g., "500 errors in the last 15 minutes").

## 2. Aggregated Summaries Table: `api_log_summaries`
*The aggregated truth for making decisions.*

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **id** | Integer | PK, Auto-increment | Unique identifier. |
| **window_start** | DateTime | Not Null | Start of the aggregation window. |
| **window_end** | DateTime | Not Null | End of the aggregation window. |
| **endpoint** | String | Not Null | The endpoint being summarized. |
| **status_code** | Integer | Not Null | The specific status code outcome. |
| **request_count** | Integer | Not Null | Total requests for this endpoint/status in this window. |
| **avg_latency** | Float | Not Null | Average latency for this grouping. |
| **error_count** | Integer | Not Null | Total errors for this grouping. |

### 💡 Philosophy
- **Raw logs** are for **forensics** (checking individual failing requests).
- **Summaries** are for **decisions** (spotting trends, spikes in latency, or error rates).
- We pre-calculate summaries to avoid expensive `COUNT(*)` and `AVG()` queries on millions of raw rows later.
