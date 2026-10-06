"""``python -m vetting [--db PATH] {ingest,review,serve} ...``"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import TextIO

from vetting.errors import NotFoundError, VettingError
from vetting.metrics import metrics
from vetting.pipeline import Pipeline
from vetting.settings import DEFAULT_DB, check_tenant_id
from vetting.store import Store
from vetting.timeline import build_timeline
from vetting.timeutil import to_iso


def _store(args: argparse.Namespace) -> Store:
    return Store.open(args.db)


def cmd_ingest(args: argparse.Namespace, out: TextIO) -> int:
    store = _store(args)
    try:
        result = Pipeline.for_tenant(check_tenant_id(args.tenant), store).ingest(Path(args.root))
    finally:
        store.close()
    print(
        f"tenant={args.tenant} identities={result.identities} observations_added={result.observations} "
        f"reviews={result.reviews}",
        file=out,
    )
    for name, count in metrics.snapshot().items():
        print(f"metric {name}={count}", file=out)
    return 0


def cmd_review(args: argparse.Namespace, out: TextIO) -> int:
    tenant = check_tenant_id(args.tenant)
    store = _store(args)
    try:
        identity = store.identities.get(tenant, args.identity_id)
        review = store.reviews.get(tenant, args.identity_id)
        if identity is None or review is None:
            raise NotFoundError(f"no review for {args.identity_id!r} in tenant {tenant!r}")
        observations = store.observations.for_identity(tenant, identity.id)
        print(f"{identity.display_name} ({identity.id})", file=out)
        print(f"recommendation: {review.recommendation.value}  score: {review.score}", file=out)
        for entry in build_timeline(identity, observations, review.findings):
            print(f"  {to_iso(entry.ts)}  [{entry.source}] {entry.text}  <{entry.ref}>", file=out)
    finally:
        store.close()
    return 0


def cmd_serve(args: argparse.Namespace, out: TextIO) -> int:
    from vetting.api.app import create_app, serve

    serve(create_app(args.db), args.host, args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vetting", description="Candidate identity vetting")
    parser.add_argument("--db", default=os.environ.get("VETTING_DB", str(DEFAULT_DB)), help="SQLite path")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="ingest a fixtures-style directory and review everyone")
    ingest.add_argument("root")
    ingest.add_argument("--tenant", required=True)
    ingest.set_defaults(func=cmd_ingest)

    review = sub.add_parser("review", help="print one identity's review and evidence timeline")
    review.add_argument("identity_id")
    review.add_argument("--tenant", required=True)
    review.set_defaults(func=cmd_review)

    serve_cmd = sub.add_parser("serve", help="run the HTTP API")
    serve_cmd.add_argument("--host", default="127.0.0.1")
    serve_cmd.add_argument("--port", type=int, default=8080)
    serve_cmd.set_defaults(func=cmd_serve)
    return parser


def main(argv: list[str] | None = None, out: TextIO | None = None) -> int:
    out = out or sys.stdout
    args = build_parser().parse_args(argv)
    try:
        return args.func(args, out)
    except VettingError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
