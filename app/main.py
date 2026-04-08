from fastapi import FastAPI , Request , Response , HTTPException , status
from prometheus_client import Counter , Histogram , generate_latest
from space_data import UNIVERSES, CREW_STATUS, AI_MOODS, ASCII_SHIPS, PLANETS, TRANSMISSIONS, ANOMALIES
import time 
from uuid import uuid4
from datetime import datetime 
import socket 
import random 

app = FastAPI()
INSTANCE_ID = socket.gethostname()



REQUEST_COUNT = Counter(
    name="http_requests_total",
    documentation="Total HTTP Requests",
    labelnames= ["method","endpoint","status"]
)

REQUEST_LATENCY = Histogram(
    name="http_request_duration_seconds",
    documentation="Request Latency",
    labelnames=["method","endpoint"],
    buckets=(0.1, 0.3, 0.5, 1, 2, 5)
)


EXCLUDE_PATHS = ["/metrics" , "/health"]



@app.middleware("http")
async def metrics_middleware(request : Request , call_next):
    path = request.url.path

    if path in EXCLUDE_PATHS:
        return await call_next(request)
    

    start = time.time()

    response : Response = await call_next(request)

    duration = time.time() - start 

    route = request.scope.get("route")
    endpoint_path = route.path if route else path

    REQUEST_COUNT.labels(
        method = request.method,
        endpoint = endpoint_path ,
        status = str(response.status_code)
    ).inc()

    REQUEST_LATENCY.labels(
        method = request.method,
        endpoint = endpoint_path
    ).observe(duration)

    print(f"[{INSTANCE_ID}] {request.method} {endpoint_path} -> {response.status_code} in {duration:.4f}s")

    return response


@app.get("/" , status_code=status.HTTP_200_OK)
def root():
    
    # Random anomaly 10% chance
    anomaly = random.choice(ANOMALIES) if random.random() < 0.1 else None

    response = {
        "mission": random.choice(UNIVERSES),
        "planet": random.choice(PLANETS),
        "ship": random.choice(ASCII_SHIPS),
        "crew_status": random.choice(CREW_STATUS),
        "ai_mood": random.choice(AI_MOODS),
        "transmission": random.choice(TRANSMISSIONS),
        "instance": INSTANCE_ID,
        "stardate": datetime.now().isoformat(),
        "request_id": str(uuid4()),
        "status": "🟢 ALL SYSTEMS NOMINAL" if not anomaly else "🔴 ANOMALY DETECTED",
        "anomaly": anomaly
    }

    return response



@app.get("/health")
def health():
    return {"status": "🟢 MISSION CONTROL ONLINE"}

@app.get("/crash")
def crash():
    if random.random() < 0.5:
        return {"detail": "🟢 SYSTEM STABLE"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail="🔴 SYSTEM FAILURE")
    


@app.get("/load")
def load(iterations: int = 10**7):
    total = 0
    for i in range(iterations):
        total += i 
    return {"status": "🟢 Load Simulated -- Hyperdrive calibration complete", "calculation_dummy": total}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain; version=0.0.4")