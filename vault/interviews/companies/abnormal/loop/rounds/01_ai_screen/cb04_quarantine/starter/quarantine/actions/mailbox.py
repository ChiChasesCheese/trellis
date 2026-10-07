"""The mail-provider boundary. Production wires a real client; tests and the CLI use ``FakeMailbox``."""
from __future__ import annotations

from typing import Any, Protocol

from quarantine.errors import MailboxError


class Mailbox(Protocol):
    def quarantine(self, tenant_id: str, message_id: str) -> None: ...

    def release(self, tenant_id: str, message_id: str) -> None: ...

    def send_receipt(self, tenant_id: str, reporter: str, report_id: str, disposition: str) -> None:
        """Tell the person who reported a message what happened to it."""
        ...


class FakeMailbox:
    """In-memory mailbox that records every call, for tests and local runs."""

    def __init__(self, fail_receipts: bool = False):
        self.calls: list[tuple[str, str, str]] = []  # (action, tenant_id, message_id)
        self.receipts: list[dict[str, Any]] = []
        self.fail_receipts = fail_receipts

    def quarantine(self, tenant_id: str, message_id: str) -> None:
        self.calls.append(("quarantine", tenant_id, message_id))

    def release(self, tenant_id: str, message_id: str) -> None:
        self.calls.append(("release", tenant_id, message_id))

    def send_receipt(self, tenant_id: str, reporter: str, report_id: str, disposition: str) -> None:
        if self.fail_receipts:
            raise MailboxError("provider unavailable: cannot deliver receipt")
        self.receipts.append(
            {"tenant_id": tenant_id, "reporter": reporter, "report_id": report_id, "disposition": disposition}
        )

    def calls_of(self, action: str) -> list[tuple[str, str, str]]:
        return [c for c in self.calls if c[0] == action]
