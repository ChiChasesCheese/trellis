"""The locked interface, as CodeSignal ships it.

Level 1 is transcribed from the assessment photos. Levels 2-4 are (reconstructed): the photos show only one-line
summaries, so names and signatures follow the isomorphic "In-Memory Database" problem
(see ../../catalog/raw/in_memory_db_isomorph.md).
"""
from abc import ABC


class ParcelTrackingSystem(ABC):
    """
    `ParcelTrackingSystem` interface.
    """

    # ---- Level 1 (verbatim) -------------------------------------------------------------

    def set_tag(self, parcel_id: str, tag: str, value: str) -> None:
        """
        Should set or overwrite the `tag` to `value` for the parcel
        identified by `parcel_id`.
        """
        # default implementation
        pass

    def get_tag(self, parcel_id: str, tag: str) -> str | None:
        """
        Should return the value of `tag` for the parcel identified
        by `parcel_id`.
        If the parcel or tag does not exist, should return `None`.
        """
        # default implementation
        return None

    def remove_tag(self, parcel_id: str, tag: str) -> bool:
        """
        Should remove the `tag` from parcel `parcel_id`.
        Returns `True` if the tag was removed or `False` if the tag
        did not exist.
        """
        # default implementation
        return False

    # ---- Level 2 (reconstructed) --------------------------------------------------------

    def list_tags(self, parcel_id: str) -> list[str]:
        """
        Should return all tags of parcel `parcel_id` as strings
        `"<tag>(<value>)"`, sorted lexicographically by tag.
        If the parcel does not exist or has no tags, return `[]`.
        """
        # default implementation
        return []

    def list_tags_by_prefix(self, parcel_id: str, prefix: str) -> list[str]:
        """
        Same as `list_tags`, but only tags that start with `prefix`.
        """
        # default implementation
        return []

    # ---- Level 3 (reconstructed) --------------------------------------------------------
    # Timestamps across all *_at calls are guaranteed to strictly increase.

    def set_tag_at(self, parcel_id: str, tag: str, value: str, timestamp: int) -> None:
        """
        Same as `set_tag`, at `timestamp`. The tag never expires.
        """
        # default implementation
        pass

    def set_tag_at_with_ttl(
        self, parcel_id: str, tag: str, value: str, timestamp: int, ttl: int
    ) -> None:
        """
        Same as `set_tag_at`, but the tag exists only during
        `[timestamp, timestamp + ttl)`.
        """
        # default implementation
        pass

    def get_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> str | None:
        """
        Same as `get_tag`, seen at `timestamp`: an expired tag does not exist.
        """
        # default implementation
        return None

    def remove_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> bool:
        """
        Same as `remove_tag`, at `timestamp`: an expired tag does not exist,
        so removing it returns `False`.
        """
        # default implementation
        return False

    def list_tags_at(self, parcel_id: str, timestamp: int) -> list[str]:
        """
        Same as `list_tags`, only tags alive at `timestamp`.
        """
        # default implementation
        return []

    def list_tags_by_prefix_at(self, parcel_id: str, prefix: str, timestamp: int) -> list[str]:
        """
        Same as `list_tags_by_prefix`, only tags alive at `timestamp`.
        """
        # default implementation
        return []

    # ---- Level 4 (reconstructed) --------------------------------------------------------

    def checkpoint(self, timestamp: int) -> int:
        """
        Should save the state of all parcels at `timestamp`, including the
        remaining TTL of every tag. Returns the number of parcels that have
        at least one tag alive at `timestamp`.
        """
        # default implementation
        return 0

    def restore(self, timestamp: int, timestamp_to_restore: int) -> None:
        """
        Should restore the state from the latest checkpoint taken at or
        before `timestamp_to_restore`. Expiry times are recalculated from
        `timestamp`: a tag that had `r` time units left when the checkpoint
        was taken expires at `timestamp + r`. Such a checkpoint is
        guaranteed to exist.
        """
        # default implementation
        pass
