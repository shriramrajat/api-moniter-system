# LOG INGESTION STRATEGY

## 1. Core Principles
- **Asynchronous Storage**: Logging must NEVER block the main request thread. If logging slows the API, the logging system itself becomes the bottleneck/outage cause.
- **Middleware-Based**: We intercept at the application boundary, not inside individual controllers.

## 2. Middleware Logic (`logging_middleware`)
The middleware will wrapper the application and execute the following flow:
1.  **Start Clock**: Record `start_time` (high-precision).
2.  **Process Request**: `await call_next(request)` to let the app handle the logic.
3.  **Catch Exceptions**: Wrap execution in a `try/except` block to catch unhandled failures.
4.  **End Clock**: Record `end_time` and calculate `latency_ms`.
5.  **Extract Details**:
    - `method` (GET, POST, etc.)
    - `endpoint` (URL path)
    - `status_code` (Response status or 500 if caught exception)
    - `error_message` (str(e) if exception occurred, else Null)
6.  **Async Dispatch**: Fire and forget (or queue) the log entry to the database background task.

## 3. Failure Capture Strategy
We must not be blind to errors.
- **Unhandled Exceptions**: Caught by the middleware `except` block. Status defaults to 500.
- **Validation Errors (422)**: captured by standard response handling, status 422.
- **5xx Responses**: Explicitly flagged.
- **Sanitization**: Error messages will be captured, but truncated or sanitized to avoid leaking sensitive stack traces in the raw `error_message` column if necessary (though for internal monitoring, stack trace hints are useful).

## 4. Implementation Artifacts
- **Middleware**: `app/middleware/log_middleware.py`
- **Background Task**: `app/services/log_service.py` (write_log function)
