"""How many times to retry a request, and how long to wait between attempts.

`Session.send()` (sessions.py) owns the retry loop itself; this module just answers the two
questions that loop needs asked of it: "is this response/exception worth retrying?" and "how long
should I sleep before the next attempt?". Keeping that decision-making out of the loop makes both
independently testable without actually sleeping or making a request.
"""

from __future__ import annotations


class Retry:
    """A retry policy: try up to `total` times, retry only on `status_forcelist` status codes or
    a connection error, and sleep `backoff_factor * 2 ** (attempt - 1)` seconds between attempts
    (attempt 1 is the first retry, so the first sleep is exactly `backoff_factor`).
    """

    def __init__(
        self,
        total: int = 3,
        backoff_factor: float = 0.0,
        status_forcelist: tuple[int, ...] = (429, 500, 502, 503, 504),
    ):
        self.total = total
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist

    def is_retryable_status(self, status_code: int) -> bool:
        """Whether a response with this status code should be retried rather than returned."""
        return status_code in self.status_forcelist

    def backoff_time(self, attempt: int) -> float:
        """Seconds to sleep before retry attempt number `attempt` (1-indexed: the first retry)."""
        if attempt < 1:
            raise ValueError(f"attempt must be >= 1, got {attempt}")
        return self.backoff_factor * (2 ** (attempt - 1))
