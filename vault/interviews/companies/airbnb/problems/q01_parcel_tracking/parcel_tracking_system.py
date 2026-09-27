"""The locked interface, as CodeSignal ships it.

Levels 1 and 3 are transcribed from the assessment photos. Levels 2 and 4 are (reconstructed): the photos show only
one-line summaries, so names and signatures follow the isomorphic "In-Memory Database" problem
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

    # ---- Level 3 (verbatim from the third batch of photos) ------------------------------
    # The timestamp argument is non-decreasing across all operations from Level 3 onward; ttl is never negative.

    def set_tag_at(self, parcel_id: str, tag: str, value: str, timestamp: int) -> None:
        """
        Should set or overwrite the `tag` to `value` for parcel `parcel_id`
        at the given `timestamp`. A tag set with `set_tag_at` does not expire
        unless overwritten.
        """
        # default implementation
        pass

    def set_tag_with_hold(
        self, parcel_id: str, tag: str, value: str, timestamp: int, ttl: int
    ) -> None:
        """
        Should set or overwrite the `tag` to `value` for parcel `parcel_id`
        at `timestamp`, with a time-to-live of `ttl` milliseconds. The tag
        expires at `timestamp + ttl`. If `ttl` is `0`, the tag does not expire.
        """
        # default implementation
        pass

    def get_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> str | None:
        """
        Should return the value of `tag` for parcel `parcel_id` as it was at
        `timestamp`. Returns `None` if the tag did not exist or had expired at
        `timestamp`.
        """
        # default implementation
        return None

    def remove_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> bool:
        """
        Should remove the `tag` from parcel `parcel_id` only if the tag is
        currently valid at `timestamp` (exclusive expiry boundary: a tag
        expiring at `timestamp` is already expired). Returns `True` if removed,
        `False` if the parcel does not exist, the tag was never set, already
        removed, or already expired by `timestamp`.
        """
        # default implementation
        return False

    def list_tags_at(self, parcel_id: str, timestamp: int) -> list[str]:
        """
        Should return all tag-value pairs for parcel `parcel_id` that were
        valid at `timestamp`, sorted lexicographically by tag name, each
        formatted as `"tag(value)"`.
        """
        # default implementation
        return []

    def list_tags_by_prefix_at(self, parcel_id: str, prefix: str, timestamp: int) -> list[str]:
        """
        Same as `list_tags_at`, only tags that start with `prefix`.
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
