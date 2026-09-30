from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
from statistics import mean
from typing import Any

from .metrics import percentile


LOG_PATH = Path("data/logs.jsonl")


def _recent_api_records(path: Path = LOG_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=60)
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
            timestamp = datetime.fromisoformat(record["ts"].replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            continue
        if record.get("service") == "api" and timestamp >= cutoff:
            records.append(record)
    return records


def dashboard_panels(records: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    requests = [record for record in records if record.get("event") == "request_received"]
    responses = [record for record in records if record.get("event") == "response_sent"]
    failures = [record for record in records if record.get("event") == "request_failed"]
    latencies = [record["latency_ms"] for record in responses if isinstance(record.get("latency_ms"), int)]
    ttfts = [record["ttft_ms"] for record in responses if isinstance(record.get("ttft_ms"), int)]
    costs = [record["cost_usd"] for record in responses if isinstance(record.get("cost_usd"), (int, float))]
    tokens_in = sum(record.get("tokens_in", 0) for record in responses)
    tokens_out = sum(record.get("tokens_out", 0) for record in responses)
    quality = [record["quality_score"] for record in responses if isinstance(record.get("quality_score"), (int, float))]
    retrieval = [record["tool_success"] for record in records if isinstance(record.get("tool_success"), bool)]
    error_rate = (len(failures) / len(requests) * 100) if requests else 0.0
    retrieval_rate = (sum(retrieval) / len(retrieval) * 100) if retrieval else 0.0
    return [
        ("Latency & TTFT", f"P95 {percentile(latencies, 95):.0f} ms · TTFT P95 {percentile(ttfts, 95):.0f} ms", "Threshold: P95 ≤ 3000 ms"),
        ("Traffic", f"{len(requests) / 60:.2f} requests/min", "Threshold: ≥ 1 request/min"),
        ("Errors & retrieval", f"{error_rate:.1f}% errors · {retrieval_rate:.1f}% retrieval success", "Threshold: errors ≤ 2% · retrieval ≥ 90%"),
        ("Cost", f"${sum(costs):.4f}", "Threshold: total ≤ $2.50"),
        ("Tokens", f"{tokens_in:,} input · {tokens_out:,} output", "Threshold: total ≤ 50,000"),
        ("Quality", f"{mean(quality):.2f}" if quality else "No data", "Threshold: average ≥ 0.75"),
    ]


def render_dashboard() -> str:
    cards = "".join(
        f"<article><h2>{escape(title)}</h2><p>{escape(value)}</p><small>{escape(threshold)}</small></article>"
        for title, value, threshold in dashboard_panels(_recent_api_records())
    )
    return f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Day 13 Dashboard</title><style>body{{margin:0;background:#f6f7f8;color:#17202a;font-family:system-ui,sans-serif}}main{{max-width:1100px;margin:auto;padding:2rem}}p,small{{color:#52616b}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem}}article{{background:#fff;border:1px solid #d8dee4;border-radius:8px;padding:1rem}}h1,h2,p{{margin-top:0}}article p{{font-size:1.25rem;font-weight:700;color:#17202a}}</style></head><body><main><h1>Day 13 Observability Dashboard</h1><p>Window: last 60 minutes · refresh this page to update</p><section class=\"grid\" aria-label=\"Observability panels\">{cards}</section></main></body></html>"""
