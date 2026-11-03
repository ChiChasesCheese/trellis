# Fix agent — real defects found in the LLD reference solutions

Repo `/Users/chiserver/sessions/trellis`. Never commit, never spawn agents, write only the problems named here and their notes. Scratch in `/tmp/craft_fix/`. `git checkout uv.lock` whenever uv touches it.

Chi learns from these solutions, so a defect teaches a bad habit. For each item: reproduce it, fix it with the smallest change that keeps the public API, and add a regression test that fails before the fix. Add the matching behaviour to `starter.py` only if its contract changes.

Each problem under `vault/domains/low-level-design/problems/` has its code embedded verbatim in a solution article, with cards behind it. After a fix, update the article and any card that shows the old code or a claim that is no longer true, then run `uv run python scripts/check_lld_problems.py <leaf>`. Find them with `grep -rl <symbol> vault/domains/low-level-design`.

## Defects

1. `thread-pool`: a done-callback that raises kills the worker thread, so later tasks never finish. A callback's failure must not take down a worker: log it and carry on, as `concurrent.futures` does.
2. `logger`: `AsyncHandler.handle` blocks on `queue.put` while holding `_state_lock`, which deadlocks when the target handler raises and the queue is full. Do not hold that lock across a blocking put, and keep close-versus-enqueue correct.
3. `digital-wallet`: ids from a generator expression raise `ValueError: generator already executing` under concurrent transfers. Use `itertools.count` directly, or take the id under a lock. Also, `reconcile` derives the balance before taking the lock: fix the race.
4. `double-entry-ledger` (under `vault/interviews/core/low-level-design/problems/`): `_synchronized` is annotated with an undefined `_F`. Fix the name and check `typing.get_type_hints` works.
5. `task-scheduler`, `atm`: the default clock is naive `datetime.now`. Use an aware UTC clock.
6. `car-rental`: re-sorts the whole schedule on every `accepts` check. Use `bisect`.
7. `text-editor`: drops the oldest undo entry with `del self._undo[0]`. Use `deque(maxlen=...)`.
8. `amz-aws-billing`: rebuilds a list on every `version_at` call. Use `bisect` with `key=`.

Afterwards run `python3 vault/interviews/core/low-level-design/check_plan.py`, and search all other solutions for the same defects 1, 2 and 3 and fix them too. Then update `seen_in` line numbers in `research/domains/python/craft_map.json` for the files you changed, keeping everything else in it.

## Gate

`check_plan.py` all ok; `check_lld_problems.py` passes on the leaves you changed; `uv run trellis --domain low-level-design validate` 0 errors; `python3 -B scripts/check_wikilinks.py | tail -1` 0 dead links.
Reply in ≤ 6 lines: what you fixed, new tests, anything you could not reproduce, other solutions with the same defect.
