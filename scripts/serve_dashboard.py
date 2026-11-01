"""Serve sources/local/dashboard/ for a limited time, then exit.

    uv run python scripts/serve_dashboard.py --host 127.0.0.1 --port 8011 --minutes 30
"""
import argparse
import functools
import http.server
import threading
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="127.0.0.1")
ap.add_argument("--port", type=int, default=8011)
ap.add_argument("--minutes", type=float, default=30)
a = ap.parse_args()
root = Path(__file__).resolve().parents[1] / "sources/local/dashboard"
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
srv = http.server.ThreadingHTTPServer((a.host, a.port), handler)
threading.Timer(a.minutes * 60, srv.shutdown).start()
print(f"http://{a.host}:{a.port}/ for {a.minutes:g} min", flush=True)
srv.serve_forever()
print("stopped", flush=True)
