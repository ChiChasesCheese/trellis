"""``python -m sentinel <command>``."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from sentinel import metrics
from sentinel.alerts import AlertRepository, AlertStatus
from sentinel.app import create_app
from sentinel.errors import SentinelError
from sentinel.config import DEFAULT_DB
from sentinel.rules import RULES


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sentinel")
    sub = p.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="collect events from a directory and raise alerts")
    ingest.add_argument("root", type=Path)
    ingest.add_argument("--tenant", required=True)
    ingest.add_argument("--db", type=Path, default=DEFAULT_DB)

    alerts = sub.add_parser("alerts", help="list a tenant's alerts, highest score first")
    alerts.add_argument("--tenant", required=True)
    alerts.add_argument("--db", type=Path, default=DEFAULT_DB)
    alerts.add_argument("--status", choices=[s.value for s in AlertStatus])
    alerts.add_argument("--limit", type=int, default=20)

    sub.add_parser("rules", help="list registered detection rules")

    serve = sub.add_parser("serve", help="run the HTTP API")
    serve.add_argument("--db", type=Path, default=DEFAULT_DB)
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8080)
    return p


def main(argv: list[str] | None = None, out=None) -> int:
    out = out or sys.stdout
    args = _parser().parse_args(argv)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    try:
        if args.command == "rules":
            for rule_id, cls in sorted(RULES.items()):
                print(f"{rule_id:20} {cls.title}", file=out)
            return 0
        app = create_app(db_path=args.db)
        if args.command == "ingest":
            alerts = app.pipeline.ingest_dir(args.root, args.tenant)
            print(
                f"ingested {metrics.total('pipeline.events')} events, {len(alerts)} alerts"
                f" ({metrics.total('collector.bad_record')} bad records skipped)",
                file=out,
            )
        elif args.command == "alerts":
            status = AlertStatus(args.status) if args.status else None
            for a in AlertRepository(app.conn).list(args.tenant, status=status, limit=args.limit):
                print(f"{a.id}  {a.threat_level.name:8} {a.score:10.4g}  {a.status.value:6}  {a.title}", file=out)
        elif args.command == "serve":
            from wsgiref.simple_server import make_server

            print(f"listening on http://{args.host}:{args.port}", file=out)
            make_server(args.host, args.port, app.wsgi).serve_forever()
    except SentinelError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
