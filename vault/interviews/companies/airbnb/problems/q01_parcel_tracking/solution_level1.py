"""Level 1 standard answer: exactly what Level 1 needs, nothing for later levels.

Paste into CodeSignal's parcel_tracking_system_impl.py. Test: IMPL=solution_level1 python3 -m unittest tests.test_level_1
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
