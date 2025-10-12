# Vercel Latency Checker

This project is a FastAPI application designed to be deployed on Vercel. It calculates latency statistics based on provided telemetry data.

## API Endpoint

The main endpoint is `/`, which accepts `POST` requests.

### Request Body

The request body should be a JSON object with the following structure:

```json
{
  "regions": ["iad1", "sfo1"],
  "threshold_ms": 100
}
```

- `regions`: A list of regions to check latency for.
- `threshold_ms`: A latency threshold in milliseconds.

### Response Body

The response will be a JSON object containing latency statistics for the specified regions.

```json
{
  "iad1": {
    "avg_latency": 50.5,
    "p95_latency": 80.2,
    "avg_uptime": 0.999,
    "breaches": 5
  },
  "sfo1": {
    "avg_latency": 120.3,
    "p95_latency": 150.8,
    "avg_uptime": 0.998,
    "breaches": 12
  }
}
```

## Local Development

To run this project locally, follow these steps:

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**

    ```bash
    uvicorn api.index:app --reload
    ```

The application will be available at `http://127.0.0.1:8000`.