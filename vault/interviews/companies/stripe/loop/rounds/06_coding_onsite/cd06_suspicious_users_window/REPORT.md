# cd06 Suspicious Users Sliding Window — report

## Summary
Classic fraud-triage sliding window: flag a user if any 60-second window anchored at one of their
own transactions contains more than 3 transactions. The interview explicitly asks for the
O(n^2) -> O(n log n) upgrade (naive per-transaction count -> sort + two-pointer), which is the
actual skill being tested — the domain framing (Radar-style burst detection) is secondary to
demonstrating that upgrade and reasoning about window boundaries precisely.

## Sources & confidence
high for the core rule ("> 3 transactions in a 1-minute window", naive-then-hashmap/window
upgrade) — one source, but an almost-verbatim interview-experience recap (rare for this repo).
The exact I/O protocol (`PART n` header, CSV row shape, `user_id: count in [start, end]` format
for Part 2, closed-interval `[t-60, t]` window definition, "first trigger" semantics) is this
repo's own reconstruction, since the source is one recap sentence with no I/O sample at all —
flagged explicitly in problem.md's Clarifications.

## Approach by part
1. Part 1: interview-legal naive approach is O(n^2) per user (for every transaction, count how
   many of the user's own transactions fall in its trailing 60s window). The reference solution
   instead reuses the Part 2 engine (see below) since it's strictly cheaper and gives identical
   results — noted in solution.py's module docstring so it doesn't read as "the naive answer was
   secretly skipped".
2. Part 2: group by `user_id`, sort each user's timestamps, then a single forward-only two-pointer
   scan (`_first_trigger`): the left pointer only ever advances past timestamps that fall outside
   `[t-60, t]` as the right pointer `t` walks forward. The first `t` where `count = j - i + 1`
   reaches 4 is returned immediately — this is provably the earliest-triggering window in time
   order because the left pointer never moves backward and every earlier `t` was already checked
   and found `< 4`.

## Pitfalls hidden tests target
- `> 3` means `>= 4`, not `>= 3` — a single off-by-one flips every boundary case.
- The window is closed (`<= 60` inclusive), so two transactions exactly 60s apart both count, but
  61s apart does not — tested with an otherwise-identical 4-transaction cluster that differs only
  in whether the last gap is 60s or 61s.
- Duplicate timestamps: several transactions sharing one instant all count individually, and the
  reported window can collapse to `start_ts == end_ts`; the *count* reported at first trigger is
  exactly the threshold (4), not the eventual burst size (5), because Part 2 must report the
  FIRST trigger, not the largest one it could eventually observe.
- A user with two separate qualifying bursts (an early modest one, a later much denser one) must
  report the early one — a naive "find the window with the maximum count" implementation would
  silently report the wrong (denser, later) burst instead of the first one.
- Input arrives out of order, both across users and within one user's own records — grouping and
  per-user sorting is mandatory, not an optimization; a solution that windows over raw input order
  will miscount.
- Part 1 and Part 2 have deliberately different output shapes (bare `user_id` vs.
  `user_id: count in [start, end]`) — not a subset/superset of one another.

## Complexity & measured cost
O(n log n): one global parse O(n), a sort per user (sum of per-user sorts is O(n log n) in the
worst case when one user holds most of the rows, still bounded by the overall n log n), then one
O(n) two-pointer pass total across all users. Perf test: 1,000,000 rows across 200,000 users,
random timestamps over a 10,000,000s range — measured well under the 2 s / 256 MB budget on
CPython 3.12 (typically ~0.6-0.9 s, well under 100 MB), dominated by string parsing, not the
windowing itself.

## Test inventory
18 tests — part1: 8 (incl. 1 io) · part2: 10 (incl. 1 io, 1 perf); edge: 6 · fmt: 2 · io: 2 ·
perf: 1.

## Skills exercised
S02 parsing (CSV, out-of-order) · S04 grouping by key · S05 sliding-window / two-pointer ·
S08 deterministic tie-break under sort · S09 exact output formatting · S17 complexity upgrade
(O(n^2) -> O(n log n), justified not just coded) · S19 incremental design (naive -> optimal, same
detection rule)

## 边写边说什么
1. **拿到题面先问三件事**：窗口是"以每笔交易为锚点向后看 60 秒"还是"任意 60 秒滑动窗口"（本题定死
   前者，因为只有锚点式定义才能让 Part 2 的"first trigger"和 `[start_ts, end_ts]` 有唯一确定的答
   案——两者对"是否超阈值"这个纯计数问题其实等价，但只有锚点式给得出具体窗口边界）；`amount` 字段
   在规则里完全不用，要不要现场问一句"它是不是给后续 follow-up 留的"；输入是否保证按时间/按用户排
   序（题面明确说不保证，分组+排序是必须步骤，不是可选优化）。
2. **写 Part 1 时**：先讲清楚"这一 part 允许 O(n²)，我先写一个能跑的版本建立信心，比如对每个用户的
   每笔交易，都去数它前 60 秒窗口里有几笔"，再补一句"如果时间允许，Part 2 我会把它换成排序+双指针"
   ——面试官想看到你知道自己在写一个暂时不是最优的版本，而不是把 O(n²) 当成终点。
3. **过渡到 Part 2 时**：主动说明双指针为什么正确——"左指针只会前进不会后退，因为一旦某个时间戳落
   在当前窗口外，它对后面所有更大的右指针位置也一定在窗口外"，这一句是证明算法复杂度是 O(n) 而不是
   "看起来是双指针但其实还是 O(n²)"的关键。
4. **讲"first trigger"语义时**：现场举一个"一个用户先来一个刚好卡线的小簇，后面又来一个更密集的大
   簇"的例子，说明为什么代码里窗口一满足阈值就要立刻 `return`，不能继续扫完整个用户找"最大"的窗口
   ——这是本题最容易被追问出 bug 的地方。
5. **交付时**：说清楚 Part 1 和 Part 2 的输出格式是有意不同的（一个只报 `user_id`，一个还报窗口和
   计数），不是"Part 2 是 Part 1 的超集"，避免面试官以为你漏了字段。
6. **被追问参数化/流式/内存上限时**（对应 problem.md「面试官会怎么追问」1/3/4 条）：直接说双指针
   算法本身不用换，只是把硬编码的 `60`/`4` 换成参数，在线场景把"整体排序"换成"每用户一个 deque，
   进出各一次"，均摊 O(1) 每事件；大量低活跃用户则提一句可以按最后活跃时间做 LRU 淘汰，不必展开实现。
## Review（2026-09-02）
- **发现（F）**：`test_perf_1m_rows` 只断言 `returncode`/耗时/内存，不断言任何输出内容——一个
  `return []` 的空桩实现瞬间跑完、内存几乎为零，能直接"通过"这个 perf 测试，属于 checklist 明确点名
  的"空洞测试"。修复：在 100 万行随机噪声里混入一个确定性的 4 笔一组、60 秒内的 `perf_marker` 突发，
  断言 `"perf_marker: 4 in [0, 30]"` 出现在输出里——既证明大规模输入下算法真的跑对了，又不需要为
  100 万行随机数据单独写一个 O(n log n) 的独立 oracle。修复前 `IMPL=starter` 该测试通过（0 failed
  贡献自它），修复后正确失败，starter 整体从 10 failed/8 passed 变为 11 failed/7 passed。
- **确认无遗留半成品**：本目录此前已有一版未完成的 review 痕迹（REPORT.md 有"边写边说什么"节但没有
  Review 节，`solution.py`/`starter*.py` 只做了 black 格式化、无逻辑改动），说明上一轮的核心审查
  已经做完、只是收尾环节被打断。本轮验证该结论成立：solution.py 的窗口语义、`_first_trigger` 的
  双指针正确性逐条核对 problem.md worked examples 后确认无 F 级 bug。
- **S 级**：未发现需要修的 S 项——函数已 ≤40 行、Part 1/2 共用 `_first_triggers`、docstring 齐全、
  problem.md 已有"面试官会怎么追问"节。
- **验证**：solution 侧 18/18 绿；starter 侧 11 failed / 7 passed（剩余 7 个通过的是"结果本就该是
  空列表/空 stdout"的负例——`test_exactly_3_not_suspicious`、`test_span_61s_...`、`test_empty_input`
  等，starter 的 `return []` 桩与正确答案巧合一致，不是断言强度不足，因为这些测试断言的是与 problem.md
  edge cases 逐条对应的精确期望值，只是那个精确期望值恰好是空)。`loop/lint.sh` 通过。
- **遗留**：无。
