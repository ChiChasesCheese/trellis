"""`python -m riskapi` serves the API with wsgiref (dev only; production runs behind gunicorn)."""
from __future__ import annotations

import logging
from wsgiref.simple_server import make_server

from .app import create_app
from .db import Database
from .settings import Settings


def main() -> None:
    settings = Settings.from_env()
    logging.basicConfig(level=logging.INFO)
    app = create_app(Database(settings.db_path), settings=settings)
    with make_server(settings.host, settings.port, app) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
