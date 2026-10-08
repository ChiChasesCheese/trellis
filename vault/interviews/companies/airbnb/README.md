# Airbnb kit

Started 2026-09-27 from one problem Chi brought in; this is **not yet a full kit**. The GitHub-first survey,
`catalog/CATALOG.md` ranking and loop guide from `building-company-interview-kits` have not been done. See `CHECKPOINT.md`.

| Path | What |
|---|---|
| `catalog/raw/` | sources, verbatim, URL + date |
| `catalog/CATALOG.md` | one row per problem (1 row so far) |
| `problems/q01_parcel_tracking/` | CodeSignal ICF 4-level problem: interface, starter, solution, 38 tests, REPORT |
| `problems/q02_banking_system/` | CodeSignal ICF 4-level problem: L1 verbatim, L2–4 reconstructed; 39 tests, 16/16 mutants killed |
| `study/essentials_codesignal_icf.md` | 中文：CodeSignal 分级模拟题心法（可迁移） |
| `study/q01_parcel_tracking.md` | 中文：q01 逐级带写 |
| `study/q02_banking_system.md` | 中文：q02 逐级带写 |

```bash
cd problems/q01_parcel_tracking
python3 -m unittest discover -s tests -p "test_*.py"                 # reference: 38/38
IMPL=starter python3 -m unittest discover -s tests -p "test_*.py"    # your starter.py
```
