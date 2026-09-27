# Raw: the isomorphic "In-Memory Database" CodeSignal ICF problem

Used to reconstruct Levels 2–4 of the parcel tracking problem. Mapping: record/key → parcel, field → tag,
backup → checkpoint. The four level summaries in the parcel photos match these four levels one-to-one.

| Source | Fetched | Confidence | What it gives |
|---|---|---|---|
| https://www.fastprep.io/problems/airbnb-in-memory-database | 2026-09-27 | medium (aggregator) | Labels the problem **Airbnb OA**. L2 `scan` returns `["<field>(<value>)", ...]` sorted lexicographically; `scanByPrefix` same format. L3 `setAtWithTtl` valid on `[timestamp, timestamp + ttl)`; "timestamps are guaranteed to strictly increase". L4 `backup(timestamp)` returns the count of non-empty non-expired records; `restore(timestamp, timestampToRestore)` restores the latest backup at or before `timestampToRestore`; "Expiration times for restored records and fields should be recalculated according to the timestamp of this operation." |
| https://www.fastprep.io/problems/coinbase-in-memory-database | not fetched (search result) | low | Same problem attributed to Coinbase. |
| https://github.com/Krishna-coder12/In-Memory-Database---OOD | 2026-09-27 | medium | Python signatures: `scan(self, key) -> list[str]`, `scan_by_prefix(self, key, prefix) -> list[str]`, `set_at`, `set_at_with_ttl(..., timestamp, ttl)`, `delete_at -> bool`, `get_at -> str | None`, `scan_at`, `scan_by_prefix_at`. L4 semantics not in its README. |
| https://csoahelp.com/2025/02/09/codesignal-in-memory-database-industry-oa/ | not fetched (search result) | low | Confirms the problem is a CodeSignal "Industry Coding" OA. |

## Reconstruction decisions (each labelled in `problem.md`)

1. Level 2 names `list_tags` / `list_tags_by_prefix` follow the Level 2 summary ("listing tags"); format from the isomorph.
2. ~~Level 3 names add `_at` / `_at_with_ttl`, as in the isomorph.~~ Superseded: the real Level 3 spec is now transcribed
   (third batch). The TTL method is `set_tag_with_hold`, `ttl == 0` never expires, timestamps are non-decreasing.
3. Level 4 names `checkpoint` / `restore` follow the Level 4 summary ("checkpoints for saving and restoring").
4. TTL recalculation on restore: remaining lifetime at checkpoint time is preserved and re-anchored at the restore
   timestamp (`new_expiry = restore_ts + (expiry - checkpoint_ts)`). This is the standard reading of "recalculated
   according to the timestamp of this operation".
