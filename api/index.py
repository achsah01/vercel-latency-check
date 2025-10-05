from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
import json
import statistics

app = FastAPI()

# Forceful CORS middleware to allow all origins and handle OPTIONS preflight
@app.middleware("http")
async def force_cors(request: Request, call_next):
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return Response(status_code=204, headers=headers)

    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# Load telemetry data once on startup
with open("q-vercel-latency.json") as f:
    telemetry_data = json.load(f)

@app.post("/")
async def check_latency(request: Request):
    body = await request.json()
    regions = body.get('regions', [])
    threshold_ms = body.get('threshold_ms', 0)

    results = {}

    for region in regions:
        region_data = [r for r in telemetry_data if r['region'] == region]
        latencies = [r['latency_ms'] for r in region_data]
        uptimes = [r['uptime_pct'] for r in region_data]
        breaches = sum(1 for r in region_data if r['latency_ms'] > threshold_ms)

        if latencies:
            avg_latency = statistics.mean(latencies)
            p95_latency = statistics.quantiles(latencies, n=100)[94]
            avg_uptime = statistics.mean(uptimes)
        else:
            avg_latency = p95_latency = avg_uptime = 0

        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 3),
            "breaches": breaches
        }

    return results
