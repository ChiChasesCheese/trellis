"""``python -m filevault serve | upload | ls``."""
from __future__ import annotations

import argparse
import mimetypes
import sys
from collections.abc import Sequence
from pathlib import Path
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

from filevault.app import App, create_app
from filevault.errors import FileVaultError
from filevault.logging_setup import configure_logging
from filevault.maintenance import fsck


class _ThreadingServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


class _QuietHandler(WSGIRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="filevault")
    parser.add_argument("--data-dir", type=Path, help="override data_dir from the config")
    sub = parser.add_subparsers(dest="command", required=True)

    serve = sub.add_parser("serve", help="run the HTTP API")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)

    upload = sub.add_parser("upload", help="store a local file for a user")
    upload.add_argument("path", type=Path)
    upload.add_argument("--user", required=True)

    sub.add_parser("fsck", help="compare the database with the blob store")

    ls = sub.add_parser("ls", help="list a user's files, newest first")
    ls.add_argument("--user", required=True)
    return parser


def _upload(app: App, args: argparse.Namespace) -> int:
    data = args.path.read_bytes()
    content_type = mimetypes.guess_type(args.path.name)[0] or "application/octet-stream"
    record = app.service.upload(args.user, args.path.name, content_type, data)
    print(f"{record.id}  {record.size}  {record.filename}")
    return 0


def _ls(app: App, args: argparse.Namespace) -> int:
    cursor: str | None = None
    while True:
        records, cursor = app.service.list_files(args.user, cursor)
        for r in records:
            print(f"{r.id}  {r.size:>10}  {r.filename}")
        if cursor is None:
            return 0


def _fsck(app: App, args: argparse.Namespace) -> int:
    report = fsck(app.service.files, app.store)
    for path in report.missing:
        print(f"missing  {path}")
    for path in report.orphaned:
        print(f"orphaned {path}")
    if report.clean:
        print("ok")
    return 0 if report.clean else 2


def _serve(app: App, args: argparse.Namespace) -> int:
    with make_server(args.host, args.port, app.wsgi, _ThreadingServer, _QuietHandler) as server:
        print(f"filevault listening on http://{args.host}:{args.port}", file=sys.stderr)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            return 0
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging()
    app = create_app(args.data_dir)
    try:
        handler = {"serve": _serve, "upload": _upload, "ls": _ls, "fsck": _fsck}[args.command]
        return handler(app, args)
    except FileVaultError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        app.close()
