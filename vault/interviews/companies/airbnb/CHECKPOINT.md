# CHECKPOINT — Airbnb kit

**State (2026-09-27):** q01 Parcel Tracking done and verified: reference 36/36 green (Level 1 cases 01–04 and the Level 3 spec + examples copied from the real assessment), empty starter red on every
level, 11/11 mutants killed; Chinese study articles written. Chi is working through it level by level in `starter.py`.

**Not done (the kit procedure, in order):**
1. GitHub-first survey → `catalog/raw/github_repos.md`; `lc_company.py Airbnb` for LeetCode originals.
2. Web sources (1p3a, LeetCode Discuss, aggregators) → `catalog/raw/`.
3. `CATALOG.md` ranked with `tools/pareto.py` (copy `tools/`, `conftest.py`, `pytest.ini` from `companies/snowflake/`).
4. `LOOP_GUIDE.md` per round.

**Next action:** Chi finishes Level 1–4 in `problems/q01_parcel_tracking/starter.py`
(`IMPL=starter python3 -m unittest tests.test_level_N`); then decide whether to run step 1.
