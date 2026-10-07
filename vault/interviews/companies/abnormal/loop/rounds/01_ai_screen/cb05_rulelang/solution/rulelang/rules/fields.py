"""What a rule may read. Field paths are resolved here, once, when the rule is loaded."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Any

from rulelang.addresses import domain_of, host_of, is_internal
from rulelang.models import Event

if TYPE_CHECKING:
    from rulelang.intel import IntelStore

STR, NUM, BOOL, STRINGS = "str", "num", "bool", "strings"


@dataclass(frozen=True)
class Scope:
    """The values one rule evaluation sees."""

    event: Event
    intel: "IntelStore"
    internal_domains: tuple[str, ...]
    bindings: dict[str, str] = field(default_factory=dict)

    def bind(self, name: str, value: str) -> "Scope":
        return replace(self, bindings={**self.bindings, name: value})


@dataclass(frozen=True)
class FieldSpec:
    type: str
    get: Callable[[Scope], Any]
    loop: str | None = None  # set when the field only exists inside any(...) over this variable


def _age(scope: Scope) -> int | None:
    return scope.intel.domain_age_days(scope.event.actor_domain)


FIELDS: dict[str, FieldSpec] = {
    "kind": FieldSpec(STR, lambda s: s.event.kind),
    "subject": FieldSpec(STR, lambda s: s.event.subject),
    "recipients": FieldSpec(STRINGS, lambda s: s.event.recipients),
    "recipient_count": FieldSpec(NUM, lambda s: len(set(s.event.recipients))),
    "sender.address": FieldSpec(STR, lambda s: s.event.actor),
    "sender.domain": FieldSpec(STR, lambda s: s.event.actor_domain),
    "sender.domain_age_days": FieldSpec(NUM, _age),
    "sender.internal": FieldSpec(BOOL, lambda s: is_internal(s.event.actor, s.internal_domains)),
    "link.url": FieldSpec(STR, lambda s: s.bindings["link"], loop="link"),
    "link.host": FieldSpec(STR, lambda s: host_of(s.bindings["link"]), loop="link"),
    "recipient.address": FieldSpec(STR, lambda s: s.bindings["recipient"], loop="recipient"),
    "recipient.domain": FieldSpec(STR, lambda s: domain_of(s.bindings["recipient"]), loop="recipient"),
    "intel.bad_hosts": FieldSpec(STRINGS, lambda s: s.intel.bad_hosts),
    "intel.vendors": FieldSpec(STRINGS, lambda s: s.intel.vendors),
}

# any(...) iterates over the one loop variable its body mentions.
LOOP_ITEMS: dict[str, Callable[[Event], tuple[str, ...]]] = {
    "link": lambda e: e.links,
    "recipient": lambda e: e.recipients,
}
