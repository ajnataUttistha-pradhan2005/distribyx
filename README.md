# Distribyx — Distributed Load-Balanced Microservices System

## Overview

Distribyx is a containerized distributed system that simulates real-world backend infrastructure. It demonstrates load balancing, observability, and system behavior under stress using modern DevOps tooling.

The system consists of multiple FastAPI service instances behind an Nginx load balancer, with Prometheus for metrics collection and Grafana for visualization.

---

## Architecture

Client requests are routed through a load balancer to multiple backend services:

```text
Client → Nginx (Load Balancer) → FastAPI Instances (app1, app2, app3)
                                      ↓
                                 Prometheus
                                      ↓
                                   Grafana
```

---

## Tech Stack

* **Backend:** FastAPI
* **Containerization:** Docker
* **Orchestration:** Docker Compose
* **Load Balancing:** Nginx
* **Monitoring:** Prometheus
* **Visualization:** Grafana

---

## Features

* Multi-instance backend (3 replicas)
* Round-robin load balancing via Nginx
* Real-time metrics collection
* Dashboard visualization (RPS, latency, errors)
* Load testing with CPU-intensive endpoints
* Observability under stress
* Deployment automation scripts

---

## Project Structure

```text
distribyx/
│
├── app/                     # FastAPI application
│   ├── main.py
│   ├── space_data.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── nginx/
│   └── nginx.conf          # Load balancer configuration
│
├── monitoring/
│   └── prometheus.yml      # Metrics configuration
│
├── compose/
│   └── docker-compose.yml  # Service orchestration
│
├── scripts/
│   ├── deploy.sh           # Deploy system
│   ├── stop.sh             # Stop services
│   ├── logs.sh             # View logs
│   └── status.sh           # Check status
│
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

* Docker
* Docker Compose
* Git

---

## Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/ajnataUttistha-pradhan2005/distribyx.git
cd distribyx
```

### 2. Start the System

```bash
docker-compose -f compose/docker-compose.yml up --build -d
```

### 3. Access Services

* Application (Load Balanced): [http://localhost:8080](http://localhost:8080)
* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)

---

## Grafana Login

```text
Username: admin
Password: admin
```

---

## Key Metrics

### Requests Per Second (RPS)

```promql
sum(rate(http_requests_total[30s]))
```

### Average Latency

```promql
rate(http_request_duration_seconds_sum[30s]) 
/
rate(http_request_duration_seconds_count[30s])
```

### Error Rate

```promql
sum(rate(http_requests_total{status="500"}[30s]))
```

---

## Load Testing

Example Python script:

```python
import requests
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8080/load"

def hit():
    try:
        requests.get(URL)
    except:
        pass

with ThreadPoolExecutor(max_workers=50) as executor:
    for _ in range(1000):
        executor.submit(hit)
```

---

## Automation Scripts

Make scripts executable:

```bash
chmod +x scripts/*.sh
```

### Deploy

```bash
./scripts/deploy.sh
```

* Pulls latest code
* Rebuilds containers
* Starts services

### Stop

```bash
./scripts/stop.sh
```

### Logs

```bash
./scripts/logs.sh
```

### Status

```bash
./scripts/status.sh
```

---

## Deployment on VM (Headless Server)

1. SSH into server:

```bash
ssh user@<vm-ip>
```

2. Deploy:

```bash
./scripts/deploy.sh
```

3. Access from browser:

```text
http://<vm-ip>:8080
http://<vm-ip>:9090
http://<vm-ip>:3000
```

---

## Observations Under Load

| Scenario             | RPS          | Latency      | Behavior       |
| -------------------- | ------------ | ------------ | -------------- |
| Light Load           | High (~300+) | Low (<1 ms)  | Fast responses |
| Heavy Load (`/load`) | Low (~8)     | High (1–3 s) | CPU-bound      |
| Errors               | 0            | Stable       | No crashes     |

---

## Key Learnings

* Load balancing distributes traffic across replicas
* Latency increases under CPU-bound workloads
* Throughput decreases as processing time increases
* Prometheus enables real-time observability
* Grafana provides actionable insights

---
