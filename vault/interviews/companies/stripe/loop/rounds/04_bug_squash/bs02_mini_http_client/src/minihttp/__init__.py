"""minihttp -- a small stdlib-only HTTP client (interview bug-squash fixture), shaped after the
public surface of `requests`: a `Session` that prepares a `Request` into wire-ready bytes, sends
it through an adapter, retries with backoff on a configurable status list, and hands back a
`Response`.

Public surface: `Session`, `Request`, `Response`, `Retry`, plus the module-level `get`/`post`
shortcuts that create a throwaway `Session`, exactly like `requests.get`/`requests.post` do.
"""

from .models import Request, Response
from .retry import Retry
from .sessions import Session

__all__ = ["Session", "Request", "Response", "Retry", "get", "post"]


def get(url: str, **kwargs) -> Response:
    return Session().get(url, **kwargs)


def post(url: str, **kwargs) -> Response:
    return Session().post(url, **kwargs)
