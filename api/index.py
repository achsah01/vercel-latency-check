from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import json
import statistics

app = FastAPI()

# Step 2: Configure CORS middleware - Paste this near the top after app = FastAPI()
origins = [
    "http://localhost:3000",  # Add your frontend URL(s) here for production
    "https://your-frontend-domain.com"  # Replace with actual domain if available
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # True if frontend sends cookies or auth headers
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 3: Handle OPTIONS preflight requests - Paste this after middleware but before route definitions
@app.options("/{rest_of_path:path}")
async def options_handler(rest_of_path: str):
    return Response(
        status_code=204,
        headers={
            "Access-Control-Allow-Origin": origins[0],  # Match the origin appropriately
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true",
        }
    )

# Load telemetry data once on startup
with open("q-vercel-latency.json") as f:
    telemetry_data = json.load(f)

@app.post("/")
async def check_latency(request):
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
