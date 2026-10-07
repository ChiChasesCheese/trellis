"""``python -m quarantine <command>``."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import Counter
from pathlib import Path
from wsgiref.simple_server import make_server

from quarantine.actions import Mailbox, drain
from quarantine.analyzers import ANALYZERS
from quarantine.app import create_app
from quarantine.config import DEFAULT_DB
from quarantine.errors import QuarantineError


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="quarantine")
    sub = p.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="file every report in a directory of JSON payloads")
    ingest.add_argument("root", type=Path)
    ingest.add_argument("--tenant", required=True)
    ingest.add_argument("--db", type=Path, default=DEFAULT_DB)

    show = sub.add_parser("show", help="print one report as JSON")
    show.add_argument("report_id")
    show.add_argument("--tenant", required=True)
    show.add_argument("--db", type=Path, default=DEFAULT_DB)

    sub.add_parser("analyzers", help="list registered analyzers")

    drain_cmd = sub.add_parser("drain-outbox", help="deliver queued receipts to reporters")
    drain_cmd.add_argument("--db", type=Path, default=DEFAULT_DB)
    drain_cmd.add_argument("--tenant", help="only this tenant (default: all)")
    drain_cmd.add_argument("--limit", type=int, default=500, help="receipts per tenant per run")

    serve = sub.add_parser("serve", help="run the HTTP API")
    serve.add_argument("--db", type=Path, default=DEFAULT_DB)
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8080)
    return p


def main(argv: list[str] | None = None, out=None, mailbox: Mailbox | None = None) -> int:
    """Run a command; ``mailbox`` lets tests observe what would be sent to the provider."""
    out = out or sys.stdout
    args = _parser().parse_args(argv)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    try:
        if args.command == "analyzers":
            for name in sorted(ANALYZERS):
                print(f"{name:20} {(ANALYZERS[name].__doc__ or '').strip().splitlines()[0]}", file=out)
            return 0
        app = create_app(db_path=args.db, mailbox=mailbox)
        try:
            if args.command == "ingest":
                seen: Counter[str] = Counter()
                for path in sorted(args.root.glob("*.json")):
                    result = app.intake.submit(args.tenant, json.loads(path.read_text()))
                    seen["duplicates" if not result.created else result.report.disposition.value] += 1
                print(
                    f"ingested {sum(seen.values())} reports: "
                    + ", ".join(f"{k}={v}" for k, v in sorted(seen.items())),
                    file=out,
                )
            elif args.command == "show":
                report = app.reports.get(args.tenant, args.report_id)
                if report is None:
                    print(f"error: no report {args.report_id} for tenant {args.tenant}", file=sys.stderr)
                    return 1
                print(json.dumps(report.to_dict(), indent=2, sort_keys=True), file=out)
            elif args.command == "drain-outbox":
                delivered = failed = 0
                for tenant in [args.tenant] if args.tenant else app.settings.tenants():
                    result = drain(app.outbox, app.mailbox, tenant, args.limit, app.actions.clock)
                    delivered, failed = delivered + result.delivered, failed + result.failed
                print(f"delivered {delivered} receipts, {failed} failed", file=out)
                if failed:
                    return 1
            elif args.command == "serve":
                print(f"serving on http://{args.host}:{args.port}", file=out)
                make_server(args.host, args.port, app.wsgi).serve_forever()
        finally:
            app.conn.close()
        return 0
    except QuarantineError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
