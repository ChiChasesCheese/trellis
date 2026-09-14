"""loop.mockserver — stdlib-only local mock servers for the Integration round.

Two servers:
  - loop.mockserver.maps      POST /render (GeoJSON-ish points -> PNG), GET /health
  - loop.mockserver.payments  Stripe-flavored /v1/charges, /v1/refunds, /v1/webhook_endpoints/test

See loop/mockserver/README.md for the endpoint reference and loop/mock.py `serve` for how a
problem's problem.md picks one via `<!-- mockserver: NAME -->`.
"""

__version__ = "0.1.0"
