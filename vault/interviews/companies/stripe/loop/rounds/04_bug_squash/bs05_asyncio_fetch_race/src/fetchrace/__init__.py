"""fetchrace -- a small bounded-concurrency async fetcher (interview bug-squash fixture).

Public surface: `fetch_all`, `Stats`, `FetchResult`, `FetchError`.
"""

from .crawler import FetchResult, Stats, fetch_all
from .http_client import FetchError

__all__ = ["fetch_all", "Stats", "FetchResult", "FetchError"]
