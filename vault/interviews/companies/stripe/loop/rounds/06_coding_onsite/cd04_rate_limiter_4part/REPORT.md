# cd04 RateLimiter (4-part) — report

## Summary
A single sliding-window-log rate limiter pushed through Stripe's recurring onsite template —
basics → memory → edge cases → concurrency — rather than the "add a new algorithm each part"
shape of this repo's other rate limiter (`problems/q23_rate_limiter`). The interesting content is
almost entirely in Parts 2-4: proving (not just claiming) an `O(limit)`-per-client memory bound,
picking and justifying one deterministic answer for every "undefined behaviour" case a naive
spec leaves open, and making the whole thing exactly correct — not just "usually fine" — under
concurrent access.

## Sources & confidence
low-medium — the 4-part structure (Basics / Saving Memory / Tricky Situations / Multiple Threads)
is directly sourced from a curled 1point3acres TOC (`loop/raw/cn_forums.md` line ~108); the body
of that page is behind a login wall, so every numeric worked example, the memory-analysis
requirement's exact wording, the specific "tricky situations" list, and the entire threading
contract in problem.md are reconstructed to be internally consistent with that TOC and with
`problems/q23_rate_limiter`'s already-sourced window-boundary convention. Treat this problem as
"the right shape, invented numbers" rather than a verbatim transcription.

## Approach by part
1. **Basics**: per-client `deque` of allowed timestamps; `allow` counts entries in
   `(t - window_ms, t]` (left-open/right-closed, matching q23) and appends `t` iff
   `count < limit`; denied calls never append. One implementation covers this and Part 2 at once —
   the "naive unbounded list" described in problem.md as the Part-1 starting point is a narrative
   device (motivating why Part 2 exists), not a second code path to maintain.
2. **Saving memory**: the deque is trimmed from the left on *every* call before counting, so it
   can never hold more than `limit` entries (denied requests are never appended, so the trim +
   append-only-on-allow combination is what makes the bound hold — not the trim alone).
   `evict_idle(now)` closes the second leak (dead clients sitting in the outer `dict` forever) by
   trimming every client's deque against `now` and dropping any that come back empty. Added
   `log_size(client_id)` purely as a testability hook so the `O(limit)`-per-active-client claim is
   asserted directly rather than inferred from timing.
3. **Tricky situations**: five behaviours pinned to one deterministic answer each — backward clock
   *clamped* per-client (not rejected, and clamping is what keeps the deque's monotonic-order
   assumption valid for the Part 2 trim logic); `limit == 0` denies unconditionally with no
   exception (it's a valid, if useless, config); same-timestamp bursts need no special case (the
   Part 1 rule already handles them correctly, in call order); `client_id == ""` is just another
   dict key; very large `t` is a non-issue in Python (arbitrary-precision ints) but worth flagging
   as language-dependent out loud.
4. **Threads**: the entire `allow`/`evict_idle` critical section (clamp → trim → count → decide →
   append/evict) is inside one `threading.Lock`, so 8 threads hammering the same client with 1000
   calls each collectively see *exactly* `limit` `True`s — proven with an exact-equality
   assertion, not a fuzzy "close enough" check. A per-client-lock design was considered and
   rejected for this exercise: it needs a *second* lock around the outer `dict` to make
   client-creation itself race-free (two threads' first call for a brand-new client both hitting
   `setdefault` is itself a race), which is real added complexity that only pays off once lock
   contention on a single global lock is actually measured to be the bottleneck — worth raising as
   a live follow-up, not worth implementing unprompted at this scale.

## Pitfalls hidden tests target
- window boundary exactly `t - window_ms` excluded, `t` included, mirrored from q23 for
  consistency across the repo's two rate limiters
- a burst of many denials must never itself extend a lockout (nothing recorded means nothing to
  expire, and nothing to inflate the next window's count either)
- `log_size` never exceeds `limit` even after 200 calls against a `limit=5` limiter — the direct,
  implementation-independent proof of the memory bound Part 2 promises
- `evict_idle` boundary (`==` window edge evicts, one ms earlier does not) and an evicted client
  coming back with a genuinely fresh budget, not a remembered exhausted one
- backward-clock clamp is per-client — one client's rollback must not leak into another's clock
- `limit == 0` never raises, always denies, including for the empty-string client
- identical-timestamp bursts resolve to exactly `min(k, remaining capacity)` allowed, in call order
- `client_id == ""` tested at the class level only — `main()`'s whitespace-split command format
  cannot represent an empty token distinctly from "no token", which is documented as a protocol
  limitation, not a class bug
- `t` at `10**15` scale behaves identically to small `t` (Python ints don't overflow)
- 8×1000 concurrent `allow()` calls against one client yield exactly `limit` successes — proves
  the lock genuinely serializes the critical section rather than merely reducing race frequency

## Complexity & measured cost
`allow`/`evict_idle` are amortised `O(1)` per call outside of `evict_idle`'s one linear pass over
currently-tracked clients (each timestamp is pushed and popped from its deque at most once).
Memory: `O(limit)` per active client, `O(limit × A)` total where `A` is clients active in the
trailing window (proven directly via `log_size`, not just argued). Perf test: 100k sequential
`allow()` calls across 2,000 clients via `run_script` — comfortably under the 2s / 256MB budget.

## Test inventory
21 tests — part1: 4 · part2: 4 · part3: 10 (incl. 2 io, 1 perf, 1 fmt) · part4: 3 (incl. one
exact-count concurrency assertion, one per-client-independence concurrency assertion, one
concurrent allow+evict_idle stress test); edge 12 · fmt 1 · io 2 · perf 1.

## Skills exercised
S03 modelling (state per client) · S05 strict/non-strict window boundaries · S12 time windows ·
S16 sliding-window log · S17 memory-bound analysis (proved, not just claimed) · S18
validation/graceful-degradation policy (clamp vs raise) · S19 incremental design · S21 stdlib
fluency (`collections.deque`, `threading.Lock`) · A15 thread-safety under contention (exact, not
approximate, correctness)

## Review（2026-09-02）
按 `loop/tasks/review_checklist.md` 逐条复核，结论：solution.py 本身在上一轮已经写得很干净，本轮只是
补齐两处遗漏，没有发现结构性问题。

**改了什么**
- `solution.py`：`allow()` 方法之前没有 docstring（`_effective_t`/`evict_idle`/`log_size` 都有，唯独
  这个核心方法没有），补了一句话 docstring 说明窗口规则和"拒绝不入账"的行为，对齐 S 项"docstring
  一句话说清做什么"以及题面里反复强调的窗口口径。
- `starter.py` / `starter_template.py`：`loop/lint.sh --fix` 后 flake8 报两个 F401（`threading`、
  `collections.deque` 未使用——这是 TODO stub 有意预留的 import，供候选人实现时用），按 checklist
  允许的方式加 `# noqa: F401` 消除，两个文件内容保持逐字一致（diff 确认 identical）。
- 其余 diff（`test_cd04.py` 里大量的空白改动）是 `loop/lint.sh --fix` 做的 black 110 列重排（注释前
  多余空格被压成两个空格），没有改动任何断言或逻辑。

**为什么**
- 这题的 4-part 结构（basics → memory → tricky edges → threads）本身已经把"未定义行为"逐条钉死、把
  内存上界用 `log_size` 直接可断言、把并发正确性用"恰好等于 limit"而不是模糊断言验证，是这批题里
  review 负担最小的一个；改动集中在文档完整性和 lint 合规，没有修复任何行为 bug。

**验证**
- solution 侧：`rtk proxy python3 -m pytest <dir> --tb=short` 连续跑 4 次（含专门为并发测试重复的 3
  次），21/21 全绿，无 flaky。
- starter 侧：`IMPL=starter rtk proxy python3 -m pytest <dir> --tb=no`，20 failed / 1 passed（唯一
  通过的是空输入测试，starter 的 `run_commands` TODO 桩本就返回 `[]`，与空输入的期望输出巧合一致，
  不是空洞测试）。
- 三个 worked examples 用 `solution.py` 直接跑了一遍，输出与 problem.md 逐字一致。
- `loop/lint.sh loop/rounds/06_coding_onsite/cd04_rate_limiter_4part` 通过（0 exit code）。

**遗留**
- 无功能性遗留项。REPORT.md 里已经讨论过的 per-client-lock 优化、分布式限流等，按原文档定位仍然是
  "面试追问话术"而非本题范围内要实现的东西，不在本轮改动范围内。
