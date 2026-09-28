"""Level 4 standard answer: solution_level3.py plus a checkpoint list and two methods.

Test: IMPL=solution_level4 python3 -m unittest discover -s tests -p "test_*.py"
"""
from parcel_tracking_system import ParcelTrackingSystem


def _alive(entry, timestamp):
    # entry = (value, expires_at). A TTL tag lives on [set time, expires_at); None = never expires / ignore expiry.
    expires_at = entry[1]
    return timestamp is None or expires_at is None or timestamp < expires_at


class ParcelTrackingSystemImpl(ParcelTrackingSystem):
    def __init__(self):
        self.parcels = {}  # parcel_id -> {tag: (value, expires_at)}
        self.checkpoints = []  # [(checkpoint_timestamp, copy of self.parcels)], oldest first

    def set_tag(self, parcel_id: str, tag: str, value: str) -> None:
        self.parcels.setdefault(parcel_id, {})[tag] = (value, None)

    def get_tag(self, parcel_id: str, tag: str) -> str | None:
        return self.get_tag_at(parcel_id, tag, None)

    def remove_tag(self, parcel_id: str, tag: str) -> bool:
        return self.remove_tag_at(parcel_id, tag, None)

    def list_tags(self, parcel_id: str) -> list[str]:
        return self.list_tags_by_prefix_at(parcel_id, "", None)

    def list_tags_by_prefix(self, parcel_id: str, prefix: str) -> list[str]:
        return self.list_tags_by_prefix_at(parcel_id, prefix, None)

    def set_tag_at(self, parcel_id: str, tag: str, value: str, timestamp: int) -> None:
        self.set_tag(parcel_id, tag, value)

    def set_tag_with_hold(
        self, parcel_id: str, tag: str, value: str, timestamp: int, ttl: int
    ) -> None:
        expires_at = None if ttl == 0 else timestamp + ttl  # the spec: ttl 0 = never expires
        self.parcels.setdefault(parcel_id, {})[tag] = (value, expires_at)

    def get_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> str | None:
        entry = self.parcels.get(parcel_id, {}).get(tag)
        if entry is None or not _alive(entry, timestamp):
            return None
        return entry[0]

    def remove_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> bool:
        tags = self.parcels.get(parcel_id)
        if tags is None or tag not in tags or not _alive(tags[tag], timestamp):
            return False
        del tags[tag]
        return True

    def list_tags_at(self, parcel_id: str, timestamp: int) -> list[str]:
        return self.list_tags_by_prefix_at(parcel_id, "", timestamp)

    def list_tags_by_prefix_at(self, parcel_id: str, prefix: str, timestamp: int) -> list[str]:
        tags = self.parcels.get(parcel_id, {})
        return [
            f"{tag}({tags[tag][0]})"
            for tag in sorted(tags)
            if tag.startswith(prefix) and _alive(tags[tag], timestamp)
        ]

    def checkpoint(self, timestamp: int) -> int:
        self.checkpoints.append((timestamp, {pid: dict(tags) for pid, tags in self.parcels.items()}))
        return sum(1 for tags in self.parcels.values() if any(_alive(e, timestamp) for e in tags.values()))

    def restore_checkpoint(self, timestamp: int, timestamp_to_restore: int) -> None:
        for checkpoint_timestamp, saved in reversed(self.checkpoints):
            if checkpoint_timestamp <= timestamp_to_restore:
                delta = timestamp - checkpoint_timestamp
                self.parcels = {
                    pid: {tag: (value, None if exp is None else exp + delta) for tag, (value, exp) in tags.items()}
                    for pid, tags in saved.items()
                }
                return
