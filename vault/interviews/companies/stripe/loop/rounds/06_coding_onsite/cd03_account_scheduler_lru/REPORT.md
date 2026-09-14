# cd03 AccountScheduler — report

## Summary
A fixed pool of sandbox accounts with timed locks (`is_available` → `acquire` → LRU
`acquire_any`), the onsite-flavoured sibling of `problems/q26_account_scheduler_lru`. The whole
exercise is class design under a 60-minute clock: one dict of `locked_until`, an explicit
exception policy (`KeyError` for unknown ids, `ValueError` for `duration <= 0`) instead of
boolean sentinels, and an LRU tie-break that intentionally uses **construction order** rather than
id string order — the detail most likely to trip up someone pattern-matching against q26.

## Sources & confidence
medium — 1point3acres 题库 "AccountScheduler LRU" (onsite, last asked 2026-03-27),
`loop/raw/en_forums.md` §6.2 (C4), linkjob 2025-12-07/2026 onsite report. The three-method
progression is well attested; the exact constructor shape, the exception-vs-sentinel choice, and
the construction-order tie-break are reconstructed for this round and marked as such in
problem.md — deliberately different from q26's dynamic-pool / id-order contract so the two
problems don't collapse into the same solution.

## Approach by part
1. `AccountScheduler(accounts)` dedupes into a list (preserves first-seen order) and builds an
   `id -> index` map for O(1) tie-break lookups. `is_available` checks membership (`KeyError` if
   absent) then `locked_until.get(id) is None or t >= locked_until[id]` (exclusive lock end).
2. `acquire` validates `duration > 0` **before** delegating to `is_available` (which is what
   raises `KeyError` for unknown ids) — the documented check order, chosen because `duration` is a
   pure argument check that needs no state lookup, so it's cheapest to run first.
3. `acquire_any` filters the fixed pool to accounts available at `t`, then `min()`s by
   `(has_been_used, last_used_or_0, construction_index)` — never-used accounts (flag 0) always
   sort before used ones (flag 1); within a group the second/third components do the ordering.
   Locking reuses the exact same `locked_until`/`last_used` writes as `acquire`.
4. `run_commands` parses the mandatory `ACCOUNTS ...` header line, then dispatches
   `AVAIL`/`ACQ`/`ANY`; any `KeyError`/`ValueError` (including `int()` failures on `t`/`duration`)
   or unknown verb/arity is caught at this layer only and printed as `ERROR` — the class itself
   never swallows an exception.

## Pitfalls hidden tests target
- exclusive lock end (`t0+d` free, `t0+d-1` not); re-lock exactly at expiry
- unknown-id `KeyError` from all three public methods, not just `is_available`
- `duration <= 0` → `ValueError`, checked before the unknown-id path even for a doubly-bad call
- never-used ranked before used regardless of "how stale" is meaningless for never-used
- never-used tie-break is **construction order** (`ACCOUNTS c b a` → `c, b, a`), not alphabetical —
  the one place this diverges hardest from q26, tested with a deliberately non-alphabetical pool
- equal `last_used` among used accounts also falls back to construction order
- failed `acquire` / plain `is_available` calls never touch `last_used`
- all-locked → `None`; the moment exactly one expires → that one, by exclusive-end comparison
- non-monotonic `t` across calls answered purely by comparison, no implicit "elapsed time" state

## Complexity & measured cost
`is_available`/`acquire` O(1). `acquire_any` is O(n) per call (linear scan + `min`) over the fixed
pool — acceptable for the onsite's stated scale and explicitly flagged in problem.md's follow-ups
as the thing to upgrade to a two-heap + lazy-invalidation design (à la q26) if asked about 10^4+
accounts under sustained load. Perf test: 100k mixed commands (50% `AVAIL`, 40% `ACQ`, 10% `ANY`)
over a 500-account pool ran in ~1.1s / ~30MB via `run_script` — comfortably under the 2s / 256MB
budget. A denser `ANY` mix (e.g. 20% over a 2,000-account pool) measured ~7.6s in ad-hoc testing,
confirming the O(n)-per-`acquire_any` follow-up is real and not just a theoretical talking point.

## Test inventory
18 tests — part1: 3 · part2: 4 · part3: 11 (incl. 2 io, 1 perf, 1 fmt); edge 8 · fmt 1 · io 2 ·
perf 1.

## Skills exercised
S03 class + dict modeling · S05 strict/non-strict time comparison · S08 deterministic tie-breaks
(construction order, not the "obvious" id order) · S10 state over an event stream · S18
validation/exception policy · S19 incremental design · S20 self-testing

## Review（2026-09-02）
**改了什么**
- `loop/lint.sh` 在改动前对本题 4 个文件全部报 "would reformat"（未跑过 black -l 110）：`--fix` 后
  `solution.py`/`starter.py`/`starter_template.py`/`test_cd03.py` 全部格式化通过，纯格式改动（多余空行、
  行内注释多空格、`test_cd03.py` 里两条 worked-example 列表从单行挤在一起改成一行一个元素），无语义变化——
  用 `git diff` 核对过，且格式化前后跑三条 worked examples 逐字核对输出不变。
- `solution.py`：`acquire` 和 `acquire_any` 原本各自重复写 `locked_until[...] = t + duration` /
  `last_used[...] = t` 这两行；抽成私有方法 `_lock(account_id, t, duration)`，两个公共方法末尾都调用它。
  公共 API（`__init__`/`is_available`/`acquire`/`acquire_any` 的签名）完全未变，`starter_template.py`/
  `starter.py`/`test_cd03.py` 不需要跟着改。
**为什么**：lint 未过是 F 项（checklist "F `loop/lint.sh <dir>` 通过"），必须修。`_lock` 抽取是 S 项
（checklist "后 part 复用前 part 的函数"）——原来 `acquire_any` 是重写一份写状态逻辑而不是复用 `acquire`
已经验证过的路径，两处逻辑分离后续容易改一处漏一处；抽取后两个公共方法的加锁写入只有一条代码路径。
`REPORT.md` 原有的 Summary/Sources/Approach/Pitfalls/Complexity/Test inventory/Skills 六节在改动前已经
符合 CONVENTIONS 要求，未改动正文，只追加本节。
**遗留**：`acquire_any` 仍是 O(pool size) 的线性扫描，problem.md 的追问 2 已经把"两个堆 + 版本号懒删除"
的优化路线写清楚，本轮按题面要求不实现，只在文章第 6 节讲清楚怎么口头带过。
