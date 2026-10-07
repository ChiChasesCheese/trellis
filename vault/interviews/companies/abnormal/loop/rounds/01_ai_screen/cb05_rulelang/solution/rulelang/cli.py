"""``python -m rulelang <command>``."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from rulelang import metrics
from rulelang.app import create_app
from rulelang.config import DEFAULT_DB
from rulelang.detectors import DETECTORS
from rulelang.errors import ConfigError, RulelangError
from rulelang.graph import CommGraph, blast_radius
from rulelang.timeutil import parse_ts


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--config-dir", type=Path, default=None)
    p.add_argument("--fixtures-dir", type=Path, default=None)


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="rulelang")
    sub = p.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="load events from a directory and run the detectors")
    run.add_argument("root", type=Path)
    run.add_argument("--tenant", required=True)
    _common(run)

    signals = sub.add_parser("signals", help="print the signals raised for one event")
    signals.add_argument("event_id")
    signals.add_argument("--tenant", required=True)
    _common(signals)

    blast = sub.add_parser("blast-radius", help="who is at risk after an account was compromised")
    blast.add_argument("account")
    blast.add_argument("--since", required=True, help="compromise time, ISO-8601")
    blast.add_argument("--tenant", required=True)
    blast.add_argument("--max-hops", type=int, default=None, help="override the tenant's [blast_radius] max_hops")
    _common(blast)

    sub.add_parser("detectors", help="list registered detectors")

    serve = sub.add_parser("serve", help="run the HTTP API")
    _common(serve)
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8080)
    return p


def main(argv: list[str] | None = None, out=None) -> int:
    out = out or sys.stdout
    args = _parser().parse_args(argv)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    try:
        if args.command == "detectors":
            for name, cls in sorted(DETECTORS.items()):
                needs = f" (requires {', '.join(cls.requires)})" if cls.requires else ""
                print(f"{name:26} {', '.join(cls.kinds)}{needs}", file=out)
            return 0
        app = create_app(db_path=args.db, config_dir=args.config_dir, fixtures_dir=args.fixtures_dir)
        if args.command == "run":
            signals = app.pipeline.ingest_dir(args.root, args.tenant)
            print(
                f"processed {metrics.total('pipeline.events')} events, {len(signals)} signals"
                f" ({metrics.total('loader.bad_record')} bad records skipped)",
                file=out,
            )
        elif args.command == "signals":
            if app.pipeline.events.get(args.tenant, args.event_id) is None:
                print(f"error: no event {args.event_id!r} for tenant {args.tenant}", file=sys.stderr)
                return 2
            for s in app.pipeline.signals.for_event(args.tenant, args.event_id):
                print(f"{s.severity.value:8} {s.detector:26} {s.summary}", file=out)
        elif args.command == "blast-radius":
            settings = app.settings.for_tenant(args.tenant)
            try:
                since = parse_ts(args.since)
            except ValueError:
                raise ConfigError("--since must be an ISO-8601 timestamp") from None
            exposures = blast_radius(
                CommGraph(app.conn, args.tenant),
                args.account,
                since,
                args.max_hops or settings.blast_radius.max_hops,
                settings.org.internal_domains,
            )
            for e in exposures:
                print(f"{e.address:34} hops={e.hops}  {' -> '.join(e.path)}", file=out)
            if not exposures:
                print("nobody at risk in the graph", file=out)
        elif args.command == "serve":
            from wsgiref.simple_server import make_server

            print(f"listening on http://{args.host}:{args.port}", file=out)
            make_server(args.host, args.port, app.wsgi).serve_forever()
    except RulelangError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
