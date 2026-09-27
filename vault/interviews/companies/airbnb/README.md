# Airbnb kit

Started 2026-09-27 from one problem Chi brought in; this is **not yet a full kit**. The GitHub-first survey,
`catalog/CATALOG.md` ranking and loop guide from `building-company-interview-kits` have not been done. See `CHECKPOINT.md`.

| Path | What |
|---|---|
| `catalog/raw/` | sources, verbatim, URL + date |
| `catalog/CATALOG.md` | one row per problem (1 row so far) |
| `problems/q01_parcel_tracking/` | CodeSignal ICF 4-level problem: interface, starter, solution, 34 tests, REPORT |
| `study/essentials_codesignal_icf.md` | 中文：CodeSignal 分级模拟题心法（可迁移） |
| `study/q01_parcel_tracking.md` | 中文：q01 逐级带写 |

```bash
cd problems/q01_parcel_tracking
python3 -m unittest discover -s tests -p "test_*.py"                 # reference: 34/34
IMPL=starter python3 -m unittest discover -s tests -p "test_*.py"    # your starter.py
```
