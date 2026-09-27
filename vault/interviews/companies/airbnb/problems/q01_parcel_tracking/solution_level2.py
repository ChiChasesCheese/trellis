"""Level 2 standard answer: solution_level1.py plus two listing methods, nothing for later levels.

Test: IMPL=solution_level2 python3 -m unittest tests.test_level_1 tests.test_level_2
"""
from parcel_tracking_system import ParcelTrackingSystem


class ParcelTrackingSystemImpl(ParcelTrackingSystem):
    def __init__(self):
        self.parcels = {}  # parcel_id -> {tag: value}

    def set_tag(self, parcel_id: str, tag: str, value: str) -> None:
        self.parcels.setdefault(parcel_id, {})[tag] = value

    def get_tag(self, parcel_id: str, tag: str) -> str | None:
        return self.parcels.get(parcel_id, {}).get(tag)

    def remove_tag(self, parcel_id: str, tag: str) -> bool:
        tags = self.parcels.get(parcel_id)
        if tags is None or tag not in tags:
            return False
        del tags[tag]
        return True

    def list_tags(self, parcel_id: str) -> list[str]:
        return self.list_tags_by_prefix(parcel_id, "")

    def list_tags_by_prefix(self, parcel_id: str, prefix: str) -> list[str]:
        tags = self.parcels.get(parcel_id, {})
        return [f"{tag}({tags[tag]})" for tag in sorted(tags) if tag.startswith(prefix)]
