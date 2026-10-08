# CHECKPOINT — Airbnb kit

**State (2026-09-27):** q01 Parcel Tracking done and verified: reference 38/38 green; all four levels follow the real spec (Levels 1, 3, 4 from photos, Level 2 from the real interface), empty starter red on every
level, 11/11 mutants killed; Chinese study articles written. Chi is working through it level by level in `starter.py`.

**State (2026-10-08):** q02 Banking System added from 7 photos Chi brought in: Level 1 verbatim, Levels 2–4
reconstructed from GitHub versions (FazeelUsmani/Industry-Problems matches the four summaries). Reference 39/39,
`solution_levelN.py` passes exactly Levels 1..N, empty starter red on every level, `mutation_check.py` 16/16 killed;
Chinese walkthrough `study/q02_banking_system.md`. Chi is doing it level by level in `starter.py`.

**Not done (the kit procedure, in order):**
1. GitHub-first survey → `catalog/raw/github_repos.md`; `lc_company.py Airbnb` for LeetCode originals.
2. Web sources (1p3a, LeetCode Discuss, aggregators) → `catalog/raw/`.
3. `CATALOG.md` ranked with `tools/pareto.py` (copy `tools/`, `conftest.py`, `pytest.ini` from `companies/snowflake/`).
4. `LOOP_GUIDE.md` per round.

**Next action:** Chi works q02 Level 1 → 4 in `problems/q02_banking_system/starter.py`
(`IMPL=starter python3 -m unittest tests.test_level_N`). Earlier: Chi finishes Level 1–4 in `problems/q01_parcel_tracking/starter.py`
(`IMPL=starter python3 -m unittest tests.test_level_N`); then decide whether to run step 1.
