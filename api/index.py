from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import json
import statistics

app = FastAPI()

# CORS middleware configuration (step 2)
origins = [
    "http://localhost:3000",            # add your frontend origin(s)
    "https://your-frontend-domain.com" # replace with your actual domain(s)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # set True if frontend sends cookies/credentials
    allow_methods=["*"],
    allow_headers=["*"],
)

# OPTIONS preflight handler (step 3)
@app.options("/{rest_of_path:path}")
async def options_handler(rest_of_path: str):
    return Response(
        status_code=204,
        headers={
            "Access-Control-Allow-Origin": origins[0],  # allow first origin
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true",
        }
    )

# Load telemetry data on startup
with open("q-vercel-latency.json") as f:
    telemetry_data = json.load(f)

# Main POST route with latency check
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
