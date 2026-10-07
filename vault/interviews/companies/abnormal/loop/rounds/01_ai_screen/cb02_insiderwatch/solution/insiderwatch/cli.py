"""Command line: `python -m insiderwatch <replay|alerts|cases|outbox|risk|export|check> ..."""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Sequence

from .alerts import AlertStore
from .alerts.cases import CaseStore
from .check import check_raw_dir, unregistered_sources
from .config import Config, load_config
from .db import open_db
from .errors import InsiderWatchError
from .export import export_alerts
from .hr import Roster
from .notify import build_notifier
from .notify.slack_webhook import read_outbox
from .pipeline import Pipeline, build_connectors
from .report import render_risk_table, risk_table
from .scoring import severity_label
from .timeutil import parse_date
from datetime import datetime, timezone


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="insiderwatch")
    parser.add_argument("--config", help="TOML file overriding defaults")
    parser.add_argument("--db", help="SQLite path (default: config db_path)")
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    replay = sub.add_parser("replay", help="process raw audit logs up to a date")
    replay.add_argument("raw_dir", type=Path)
    replay.add_argument("--until", required=True, help="YYYY-MM-DD, inclusive (UTC)")
    replay.add_argument("--hr", type=Path, help="roster JSON (default: <raw_dir>/../hr/roster.json)")
    replay.add_argument("--notifier", choices=["console", "slack"])
    replay.add_argument("--reset", action="store_true", help="delete the database first")
    replay.add_argument("--json", action="store_true", help="print the summary as JSON")

    alerts = sub.add_parser("alerts", help="list alerts")
    alerts.add_argument("--user")
    alerts.add_argument("--json", action="store_true")

    cases = sub.add_parser("cases", help="list alert cases, or `cases close <id>`")
    cases.add_argument("action", nargs="?", choices=["close"])
    cases.add_argument("case_id", nargs="?", type=int)
    cases.add_argument("--user")
    cases.add_argument("--json", action="store_true")

    outbox = sub.add_parser("outbox", help="show queued notifications")
    outbox.add_argument("--json", action="store_true")

    risk = sub.add_parser("risk", help="per-user decayed risk ranking")
    risk.add_argument("--as-of", help="YYYY-MM-DD (default: now)")

    export = sub.add_parser("export", help="dump alerts for a SIEM")
    export.add_argument("--format", choices=["jsonl", "csv"], default="jsonl")

    check = sub.add_parser("check", help="dry-run connectors over a raw directory")
    check.add_argument("raw_dir", type=Path)
    return parser


def _db_path(args: argparse.Namespace, config: Config) -> str:
    return args.db or config.db_path


def cmd_replay(args: argparse.Namespace, config: Config) -> int:
    db_path = _db_path(args, config)
    if args.reset and os.path.exists(db_path):
        os.remove(db_path)
    conn = open_db(db_path)
    hr_path = args.hr or args.raw_dir.parent / "hr" / "roster.json"
    roster = Roster.load(hr_path) if Path(hr_path).exists() else Roster.empty()
    notifier = build_notifier(args.notifier or config.notifier, conn, config)
    pipeline = Pipeline(conn, config, roster, build_connectors(args.raw_dir, config), notifier)
    summary = pipeline.run(parse_date(args.until)).to_dict()
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"{summary['events']} events over {summary['days']} days, {summary['alerts']} alerts")
        for source, count in sorted(summary["by_source"].items()):
            print(f"  {source}: {count} events, {summary['dropped'].get(source, 0)} dropped")
    return 0


def cmd_alerts(args: argparse.Namespace, config: Config) -> int:
    alerts = AlertStore(open_db(_db_path(args, config))).list(user=args.user)
    rows = [{**a.to_dict(), "severity": severity_label(a.score, config)} for a in alerts]
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    for row in rows:
        print(f"{row['id']:>4}  {row['ts'][:16]}  {row['user']:<28} {row['signal']:<24} "
              f"{row['score']:.2f} {row['severity']:<6} {'; '.join(row['reasons'])}")
    return 0


def cmd_cases(args: argparse.Namespace, config: Config) -> int:
    store = CaseStore(open_db(_db_path(args, config)), config)
    if args.action == "close":
        if args.case_id is None:
            raise InsiderWatchError("usage: cases close <id>")
        print(f"closed case {store.close(args.case_id).id}")
        return 0
    rows = [c.to_dict(config) for c in store.list(user=args.user)]
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    for row in rows:
        print(f"{row['id']:>4}  {row['status']:<6} {row['severity']:<6} {row['user']:<28} "
              f"{len(row['alerts'])} alerts  {row['opened_at'][:16]} .. {row['last_alert_at'][:16]}")
    return 0


def cmd_outbox(args: argparse.Namespace, config: Config) -> int:
    rows = read_outbox(open_db(_db_path(args, config)))
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        for row in rows:
            print(f"{row['id']:>4}  {row['payload']['text']}")
    return 0


def cmd_risk(args: argparse.Namespace, config: Config) -> int:
    as_of = datetime.now(timezone.utc)
    if args.as_of:
        as_of = datetime.combine(parse_date(args.as_of), datetime.max.time(), tzinfo=timezone.utc)
    alerts = AlertStore(open_db(_db_path(args, config))).list()
    print(render_risk_table(risk_table(alerts, as_of, config)))
    return 0


def cmd_export(args: argparse.Namespace, config: Config) -> int:
    alerts = AlertStore(open_db(_db_path(args, config))).list()
    sys.stdout.write(export_alerts(alerts, args.format, config))
    return 0


def cmd_check(args: argparse.Namespace, config: Config) -> int:
    print(json.dumps(check_raw_dir(args.raw_dir, config), indent=2, sort_keys=True))
    for name in unregistered_sources(args.raw_dir, config):
        print(f"warning: no connector registered for {name}/", file=sys.stderr)
    return 0


COMMANDS = {"replay": cmd_replay, "alerts": cmd_alerts, "cases": cmd_cases, "outbox": cmd_outbox,
            "risk": cmd_risk, "export": cmd_export, "check": cmd_check}


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING, stream=sys.stderr)
    try:
        return COMMANDS[args.command](args, load_config(args.config))
    except InsiderWatchError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
