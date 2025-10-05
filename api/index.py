from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import json
import statistics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

with open("q-vercel-latency.json") as f:
    telemetry_data = json.load(f)

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return Response(status_code=200)

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
