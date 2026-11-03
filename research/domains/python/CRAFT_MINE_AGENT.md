# Mining agent — what the LLD solutions have in common

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only `research/domains/python/craft_map.json`. Scratch in `/tmp/craft_mine/`. `git checkout uv.lock` whenever uv touches it.

Chi (2026-11-03) wants much stronger core coding and deeper Python: advanced idioms, architecture understanding, and above all connecting what different problems share. Your job is the map; other agents write the cards from it.

## Input

- `research/domains/python/craft_index.json` (rerun `python3 research/domains/python/craft_index.py` first): feature → problem → lines. Entries starting `~` are text matches and need checking.
- The code: `vault/domains/low-level-design/problems/*/solution.py` and `vault/interviews/core/low-level-design/problems/*/solution.py`. Their `**写法。**` sections name patterns. Read at least 35 solutions across all categories, the longest and most varied first, and open what the index points to.
- What already exists: `skeleton/python.yaml` holds the language facts (466 cards), `skeleton/low-level-design.yaml` the concepts, and `lld.cross` in `skeleton/hello-interview.yaml` five cross-question patterns. Do not plan cards that only restate a language fact: every entry must be about using something in real code.

Do not open `sources/local/hello-interview/premium/` or `cards/premium/`. This work is public.

## Output: `research/domains/python/craft_map.json`

```json
{"branches": [{"id": "idioms|patterns|architecture", "leaves": [{
  "id": "short-kebab", "title": "中文名（English）", "summary": "one line",
  "why": "the problem it solves and what the plain version costs",
  "language_leaves": ["python domain leaf ids it rests on"],
  "seen_in": [{"slug": "parking-lot", "lines": [40, 41], "how": "one line: what differs here"}],
  "scales": {"leetcode": "LC slug or empty", "lld": "drill slug", "system_design": "the same mechanism at system scale, or empty"},
  "card_ideas": ["3-6 specific questions, each a why or when, not a definition"]
}]}]}
```

- **idioms (about 25–35 leaves):** advanced Python used well in real code. Immutable views (`MappingProxyType`, frozen and slots dataclasses), functions versus Protocol for strategies, generators as pipelines, context managers for invariants, descriptors and `__init_subclass__` where they earn their place, `heapq` tuple ordering and tie-breaks, `bisect` on sorted lists, `Decimal` and integer money, `Enum` behaviour, typed errors, sentinels, `__post_init__` validation, `functools`, `match`. Include idioms the solutions should have used but do not, and say so in `why`.
- **patterns (about 25–35 leaves):** mechanisms that recur across problems regardless of language. Examples: transition-table state machines, injected clock, lazy expiry, lazy deletion in a heap, immutable snapshots, hash map plus ordered structure, per-key locks, mutate under the lock and notify outside it, version check, idempotency key storing the result, append-only log with derived state, dependency graph with cycle detection, recursive-descent parsing, pipeline of steps, policy seam. At least 3 problems in `seen_in` for each pattern, and every slug and line must be real: check them.
- **architecture (about 15–20 leaves):** reasoning above a class. Dependency direction, functional core with imperative shell, where interfaces belong, entity versus value object, transaction boundary, command versus event, where extension points are worth paying for and where they are not, seams for testing, error boundaries, and how a design changes from one process to a distributed system. Each cites real problems.

Rank leaves inside each branch by how much they raise a senior's coding, not by how often they appear. `scales` is what ties the knowledge together: fill it wherever the mechanism truly appears at that level (LRU: LC 146, `lru-cache`, a distributed cache's eviction).

## Gate

A short script confirming every `seen_in` slug exists and its lines are within the file, and that each pattern has at least 3 problems. Reply in ≤ 6 lines: leaves per branch, the 5 most valuable patterns, and any solution you think is poorly written.
