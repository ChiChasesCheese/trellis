---
nodes: [python.stdlib, chrono.parsing, chrono.arithmetic]
url: https://docs.python.org/3/library/datetime.html
tags: [docs]
---
# datetime — basic date and time types

Read this for one distinction and one table. The distinction is naive versus
aware: a `datetime` without `tzinfo` compares and subtracts happily against
another naive one and raises against an aware one, so mixing the two is a
runtime error waiting for the input that has an offset. The table is
`strftime`/`strptime` format codes, which you should be able to write without a
search — `%Y-%m-%d %H:%M:%S`, `%z`, `%j`, `%w`.

**Extract on read:**
- `fromisoformat` / `isoformat` as the fast path, and where `strptime` is still
  needed (non-ISO shapes, strict validation by round-trip).
- `timedelta` arithmetic is duration arithmetic — it has days, seconds and
  microseconds and deliberately no months.
- `date.today()` and `datetime.now()` are the classic source of a test that
  passes today ([[cc-verification-determinism-repeatable-runs]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/datetime.html)

## Archived copy
![[python-datetime-clip]]
%% trellis:end %%
