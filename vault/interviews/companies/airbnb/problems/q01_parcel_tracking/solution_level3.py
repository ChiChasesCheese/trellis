"""Level 3 standard answer: solution_level2.py refactored once for timestamps and TTL, nothing for Level 4.

The refactor: each value becomes (value, expires_at), and the Level 1/2 methods call the new *_at methods with
timestamp=None, meaning "ignore expiry".
Test: IMPL=solution_level3 python3 -m unittest tests.test_level_1 tests.test_level_2 tests.test_level_3
"""
from parcel_tracking_system import ParcelTrackingSystem


def _alive(entry, timestamp):
    # entry = (value, expires_at). A TTL tag lives on [set time, expires_at); None = never expires / ignore expiry.
    expires_at = entry[1]
    return timestamp is None or expires_at is None or timestamp < expires_at


class ParcelTrackingSystemImpl(ParcelTrackingSystem):
    def __init__(self):
        self.parcels = {}  # parcel_id -> {tag: (value, expires_at)}

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

    def set_tag_at_with_ttl(
        self, parcel_id: str, tag: str, value: str, timestamp: int, ttl: int
    ) -> None:
        self.parcels.setdefault(parcel_id, {})[tag] = (value, timestamp + ttl)

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
