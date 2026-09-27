"""Reference solution: all four levels.

Design in one sentence: every public method is a thin wrapper over a few private primitives that take an optional
`timestamp`, so Level 1/2 calls are Level 3 calls with `timestamp=None` ("ignore expiry").
"""
import bisect
from dataclasses import dataclass

from parcel_tracking_system import ParcelTrackingSystem


@dataclass
class _Tag:
    value: str
    expires_at: int | None = None  # None = never expires; alive on [set time, expires_at)

    def alive(self, timestamp: int | None) -> bool:
        return timestamp is None or self.expires_at is None or timestamp < self.expires_at


class ParcelTrackingSystemImpl(ParcelTrackingSystem):
    def __init__(self):
        self._parcels: dict[str, dict[str, _Tag]] = {}
        # Checkpoints in timestamp order (timestamps strictly increase, so appending keeps it sorted).
        self._checkpoint_times: list[int] = []
        # Each snapshot: parcel_id -> tag -> (value, remaining ttl or None). Plain tuples, never shared with live state.
        self._snapshots: list[dict[str, dict[str, tuple[str, int | None]]]] = []

    # ---- private primitives ---------------------------------------------------------------

    def _set(self, parcel_id: str, tag: str, value: str, expires_at: int | None) -> None:
        self._parcels.setdefault(parcel_id, {})[tag] = _Tag(value, expires_at)

    def _alive_tags(self, parcel_id: str, timestamp: int | None) -> dict[str, str]:
        tags = self._parcels.get(parcel_id, {})
        return {t: e.value for t, e in tags.items() if e.alive(timestamp)}

    def _get(self, parcel_id: str, tag: str, timestamp: int | None) -> str | None:
        entry = self._parcels.get(parcel_id, {}).get(tag)
        return entry.value if entry is not None and entry.alive(timestamp) else None

    def _remove(self, parcel_id: str, tag: str, timestamp: int | None) -> bool:
        tags = self._parcels.get(parcel_id)
        if tags is None or tag not in tags:
            return False
        alive = tags[tag].alive(timestamp)
        del tags[tag]  # an expired entry is garbage either way
        if not tags:
            del self._parcels[parcel_id]
        return alive

    def _list(self, parcel_id: str, prefix: str, timestamp: int | None) -> list[str]:
        alive = self._alive_tags(parcel_id, timestamp)
        return [f"{t}({alive[t]})" for t in sorted(alive) if t.startswith(prefix)]

    # ---- Level 1 --------------------------------------------------------------------------

    def set_tag(self, parcel_id: str, tag: str, value: str) -> None:
        self._set(parcel_id, tag, value, None)

    def get_tag(self, parcel_id: str, tag: str) -> str | None:
        return self._get(parcel_id, tag, None)

    def remove_tag(self, parcel_id: str, tag: str) -> bool:
        return self._remove(parcel_id, tag, None)

    # ---- Level 2 --------------------------------------------------------------------------

    def list_tags(self, parcel_id: str) -> list[str]:
        return self._list(parcel_id, "", None)

    def list_tags_by_prefix(self, parcel_id: str, prefix: str) -> list[str]:
        return self._list(parcel_id, prefix, None)

    # ---- Level 3 --------------------------------------------------------------------------

    def set_tag_at(self, parcel_id: str, tag: str, value: str, timestamp: int) -> None:
        self._set(parcel_id, tag, value, None)

    def set_tag_at_with_ttl(
        self, parcel_id: str, tag: str, value: str, timestamp: int, ttl: int
    ) -> None:
        self._set(parcel_id, tag, value, timestamp + ttl)

    def get_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> str | None:
        return self._get(parcel_id, tag, timestamp)

    def remove_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> bool:
        return self._remove(parcel_id, tag, timestamp)

    def list_tags_at(self, parcel_id: str, timestamp: int) -> list[str]:
        return self._list(parcel_id, "", timestamp)

    def list_tags_by_prefix_at(self, parcel_id: str, prefix: str, timestamp: int) -> list[str]:
        return self._list(parcel_id, prefix, timestamp)

    # ---- Level 4 --------------------------------------------------------------------------

    def checkpoint(self, timestamp: int) -> int:
        snapshot: dict[str, dict[str, tuple[str, int | None]]] = {}
        for parcel_id, tags in self._parcels.items():
            kept = {
                t: (e.value, None if e.expires_at is None else e.expires_at - timestamp)
                for t, e in tags.items()
                if e.alive(timestamp)
            }
            if kept:
                snapshot[parcel_id] = kept
        self._checkpoint_times.append(timestamp)
        self._snapshots.append(snapshot)
        return len(snapshot)

    def restore(self, timestamp: int, timestamp_to_restore: int) -> None:
        i = bisect.bisect_right(self._checkpoint_times, timestamp_to_restore) - 1
        if i < 0:
            return  # the spec guarantees a checkpoint exists; do nothing rather than crash
        self._parcels = {
            parcel_id: {
                t: _Tag(value, None if remaining is None else timestamp + remaining)
                for t, (value, remaining) in tags.items()
            }
            for parcel_id, tags in self._snapshots[i].items()
        }
