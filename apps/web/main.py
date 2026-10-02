from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

APP_ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(title="YAGBU Dashboard", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def dashboard_home() -> str:
    return """
    <html>
      <head>
        <title>YAGBU Dashboard</title>
        <style>
          body { font-family: sans-serif; background: #0b0f19; color: #e5e7eb; padding: 48px; }
          .card { background: #111827; border: 1px solid #2d3748; border-radius: 12px; padding: 24px; margin-bottom: 18px; }
          .title { font-size: 32px; font-weight: 700; margin-bottom: 8px; }
          .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 18px; }
          .metric { background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 20px; }
          .label { color: #94a3b8; font-size: 12px; text-transform: uppercase; }
          .value { font-size: 28px; font-weight: 700; margin-top: 8px; }
        </style>
      </head>
      <body>
        <div class="card">
          <div class="title">YAGBU SaaS Dashboard</div>
          <div>Model operations, usage, billing and deployment health</div>
        </div>
        <div class="grid">
          <div class="metric"><div class="label">Active Models</div><div class="value">2</div></div>
          <div class="metric"><div class="label">Deployments</div><div class="value">3</div></div>
          <div class="metric"><div class="label">Requests</div><div class="value">12.3K</div></div>
          <div class="metric"><div class="label">Cost</div><div class="value">$128</div></div>
        </div>
      </body>
    </html>
    """


@app.get("/api/overview")
def dashboard_overview() -> dict:
    return {
        "active_models": 2,
        "deployments": 3,
        "requests_total": 12300,
        "cost_usd": 128.0,
        "status": "healthy",
    }


@app.get("/api/metrics")
def metrics() -> dict:
    return {
        "latency_ms": {"p50": 420, "p95": 1800, "p99": 3400},
        "throughput_rps": 32.4,
        "error_rate": 0.004,
        "uptime_seconds": 86400,
    }


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "services": {
            "api": "healthy",
            "worker": "healthy",
            "database": "healthy",
            "redis": "healthy",
        },
    }


__all__ = ["app"]
