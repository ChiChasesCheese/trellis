"""Reference solution: the end state after all four levels.

Level 1 alone is just `dict[parcel_id, dict[tag, value]]` (see study/q01_parcel_tracking.md). Level 3 turned each value
into `(value, expires_at)` and made the Level 1/2 methods call private helpers with `timestamp=None` ("ignore expiry").
"""
import bisect

from parcel_tracking_system import ParcelTrackingSystem


def _alive(expires_at: int | None, timestamp: int | None) -> bool:
    # None = never expires / ignore expiry; a TTL tag is alive on [set time, expires_at)
    return timestamp is None or expires_at is None or timestamp < expires_at


class ParcelTrackingSystemImpl(ParcelTrackingSystem):
    def __init__(self):
        self._parcels: dict[str, dict[str, tuple[str, int | None]]] = {}  # tag -> (value, expires_at)
        # Checkpoints in timestamp order (timestamps never decrease, so appending keeps it sorted).
        self._checkpoint_times: list[int] = []
        # Each snapshot: parcel_id -> tag -> (value, remaining ttl or None). Plain tuples, never shared with live state.
        self._snapshots: list[dict[str, dict[str, tuple[str, int | None]]]] = []

    # ---- private primitives ---------------------------------------------------------------

    def _set(self, parcel_id: str, tag: str, value: str, expires_at: int | None) -> None:
        self._parcels.setdefault(parcel_id, {})[tag] = (value, expires_at)

    def _alive_tags(self, parcel_id: str, timestamp: int | None) -> dict[str, str]:
        tags = self._parcels.get(parcel_id, {})
        return {t: v for t, (v, exp) in tags.items() if _alive(exp, timestamp)}

    def _get(self, parcel_id: str, tag: str, timestamp: int | None) -> str | None:
        entry = self._parcels.get(parcel_id, {}).get(tag)
        if entry is None or not _alive(entry[1], timestamp):
            return None
        return entry[0]

    def _remove(self, parcel_id: str, tag: str, timestamp: int | None) -> bool:
        tags = self._parcels.get(parcel_id)
        if tags is None or tag not in tags:
            return False
        alive = _alive(tags[tag][1], timestamp)
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

    def set_tag_with_hold(
        self, parcel_id: str, tag: str, value: str, timestamp: int, ttl: int
    ) -> None:
        self._set(parcel_id, tag, value, None if ttl == 0 else timestamp + ttl)  # the spec: ttl 0 = never expires

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
                t: (v, None if exp is None else exp - timestamp)
                for t, (v, exp) in tags.items()
                if _alive(exp, timestamp)
            }
            if kept:
                snapshot[parcel_id] = kept
        self._checkpoint_times.append(timestamp)
        self._snapshots.append(snapshot)
        return len(snapshot)

    def restore_checkpoint(self, timestamp: int, timestamp_to_restore: int) -> None:
        i = bisect.bisect_right(self._checkpoint_times, timestamp_to_restore) - 1
        if i < 0:
            return  # the spec: no checkpoint at or before timestamp_to_restore = no effect
        self._parcels = {
            parcel_id: {
                t: (value, None if remaining is None else timestamp + remaining)
                for t, (value, remaining) in tags.items()
            }
            for parcel_id, tags in self._snapshots[i].items()
        }
