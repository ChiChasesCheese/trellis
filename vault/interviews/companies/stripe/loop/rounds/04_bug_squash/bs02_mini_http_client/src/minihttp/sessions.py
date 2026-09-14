"""Session: the object callers actually talk to. Owns default headers, the retry policy, and the
adapter that does the real sending; `.get()`/`.post()`/etc are thin wrappers around `.request()`.

The retry loop lives here (not in `retry.Retry`) because it's the one place that needs to own
"try again" side effects -- sleeping, re-sending, deciding when to give up -- while `Retry` itself
stays a pure policy object (see retry.py) that's easy to unit test on its own.
"""

from __future__ import annotations

import time

from .adapters import HTTPAdapter
from .models import Request, Response
from .retry import Retry


class Session:
    def __init__(
        self,
        headers: dict | None = None,
        retry: Retry | None = None,
        adapter: object | None = None,
        sleep=time.sleep,
    ):
        self.headers = dict(headers) if headers else {}
        self.retry = retry or Retry(total=1)
        self.adapter = adapter or HTTPAdapter()
        self._sleep = sleep

    def request(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
        data: object = None,
        json: object = None,
        files: dict | None = None,
    ) -> Response:
        merged_headers = {**self.headers, **(headers or {})}
        prepared = Request(method, url, merged_headers, params, data, json, files).prepare()

        attempt = 1
        last_response = None
        last_exc = None
        while attempt <= self.retry.total:
            try:
                response = self.adapter.send(prepared)
            except OSError as exc:
                last_exc = exc
                last_response = None
            else:
                last_exc = None
                last_response = response
                if not self.retry.is_retryable_status(response.status_code):
                    return response
            if attempt < self.retry.total:
                self._sleep(self.retry.backoff_time(attempt))
            attempt += 1

        if last_exc is not None:
            raise last_exc
        return last_response

    def get(self, url: str, **kwargs) -> Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> Response:
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> Response:
        return self.request("DELETE", url, **kwargs)
