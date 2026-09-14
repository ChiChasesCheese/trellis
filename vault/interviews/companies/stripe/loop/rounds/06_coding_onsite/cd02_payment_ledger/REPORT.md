# cd02 PaymentLedger — report

## Summary
A small class-based bookkeeping exercise from the 2026 Summer Intern VO coding round: build a
`PaymentLedger` with payments, partial refunds, revenue, and a date-range query, revealed in three
interview stages. The real difficulty is not algorithmic — it is picking, and then holding to,
one consistent error-contract: idempotent no-op (`False`) vs. `KeyError` vs. `ValueError` for
three genuinely different failure situations, plus a persistence round-trip that must preserve
enough state (including *which* refund ids were already applied) to keep enforcing the same rules
after a reload.

## CONVENTIONS 对照
This problem's source asks for a **class**, not a `partN(lines) -> list[str]` pipeline — the
method set (`add_payment`, `add_refund`, `get_total_revenue`, `get_payments_by_date`) is
cumulative across the three interview stages on *one* object, the way a real interviewer reveals
it (there is no "Part 1 class" vs. "Part 2 class"). To keep the class the primary, natural
interface while still satisfying this repo's harness contract:
- Most tests instantiate `impl.PaymentLedger()` directly and call methods — the natural shape for
  an OOP question, and still fully swappable via `IMPL=starter` since the whole module (class +
  functions) is loaded as one unit.
- `part1(lines)` / `part2(lines)` / `part3(lines)` are thin, **identical** wrappers around one
  `run_commands(lines)` command-stream engine (`PAY`/`REFUND`/`REVENUE`/`RANGE`), present solely
  so the `impl.partN(...)` and `main(stdin, stdout)` surfaces this repo's other problems rely on
  still exist here. They differ in which tests exercise them (by feature), not in implementation
  capability — documented explicitly in solution.py's docstring and here so it doesn't read as an
  oversight.

## Sources & confidence
medium-high — `loop/raw/cn_forums.md` line 104 (programhelp.net's write-up of the 2026 Summer
Intern VO) gives the method names (`Add_payment`, `Add_refund`, `Get_total_revenue`,
`Get_payments_by_date`), the payment_id-dedup rule, partial-refund support, and all five follow-up
directions verbatim. It does **not** give exact parameter names/types, the timestamp format, which
failures are exceptions vs. `False`, or persistence method signatures (`export_json`/`load_json`)
— all of that is this problem.md's own concrete, testable reconstruction, flagged explicitly in
"Variants."

## Approach by part
1. **Part 1**: a dict keyed by `payment_id`; `add_payment` returns `False` without mutating state
   on a duplicate id. `get_total_revenue` is a generator-sum over `amount - refunded` (refunded is
   always `0` until Part 2 exists, so this is a plain sum at this stage).
2. **Part 2**: `add_refund` checks, in this exact order: timestamp validity -> duplicate
   `refund_id` (idempotent `False`) -> unknown `payment_id` (`KeyError`) -> over-refund
   (`ValueError`) -> success (accumulate `refunded`, record the `refund_id`). The order matters:
   `test_refund_invalid_timestamp_raises_before_other_checks` and
   `test_duplicate_refund_id_is_idempotent_before_amount_check` pin down two orderings a candidate
   is likely to get backwards.
3. **Part 3**: `get_payments_by_date` validates both bounds, then filters on the stored *strings*
   — the fixed-width `YYYY-MM-DDTHH:MM:SS` profile makes string order == chronological order, so
   nothing is re-parsed per query. Linear scan, no index: the perf budget (10^5 payments, single
   query) never needs one; the follow-up list names bisect/index-based scaling as a discussion
   point instead. `export_json`/`load_json` round-trip both the payment records *and* the
   `refund_ids` set — losing the latter would let a reloaded ledger accept a replayed duplicate
   refund, which `test_loaded_ledger_still_enforces_refund_rules` catches directly.

## Pitfalls hidden tests target
- three distinct failure shapes for three distinct situations (idempotent `False` / `KeyError` /
  `ValueError`) — conflating any two of them is the most likely mistake.
- refund validation order: bad timestamp beats "unknown payment"; duplicate `refund_id` beats the
  over-refund check (so replaying an already-successful refund never raises, even if the payment
  has since been fully refunded by other refunds).
- exact-boundary refund (refunding precisely the remaining balance) must succeed; one cent over
  must raise — an off-by-one in `>` vs `>=` is the classic bug here.
- `get_payments_by_date` bounds are inclusive on both sides; sort tie-break is `payment_id`, not
  insertion order.
- `export_json`/`load_json` must preserve the refund-id set, not just the running totals — a
  common shortcut (persisting only `refunded_cents` per payment) silently breaks idempotency after
  a reload.
- duplicate `payment_id` must not overwrite the original amount/ts/customer — only the boolean
  return communicates the no-op.

## Complexity & measured cost
O(1) amortized for `add_payment`/`add_refund` (dict operations); O(n) for `get_total_revenue` and
`get_payments_by_date` (n = number of payments) — acceptable at the stated 10^5 scale and
explicitly not over-engineered into an index, per the follow-up list's own framing of that as a
discussion extension. 100k payments + one range query, well under the 2 s / 256 MB budget (see
`test_perf_100k_payments_and_range_query`).

## Test inventory
24 tests — part1: 6 · part2: 6 · part3: 12 (incl. 1 fmt, 3 io, 1 perf); edge 9 · fmt 1 · io 3 · perf 1.

## Skills exercised
S02 parsing/validation with a fixed timestamp profile . S03 an incrementally-revealed class API .
S06 integer-cents money . S08 deterministic multi-key sort . S09 exact output formatting . S17
error-contract design (three distinct failure shapes) . S18 validation and defensive input
handling . S20 serialization round-trip correctness

## 边写边说什么
1. **拿到题面先问三件事**：金额是分还是浮点美元（本题定死整数分，但真实面试要主动问）；时间戳格式
   是不是统一的 ISO 8601（本题定死一种 profile，说明理由：字符串排序要和时间排序一致）；
   `payment_id`/`refund_id` 重复算错误还是算幂等重试——这直接决定返回值设计。
2. **写 Part 1 时**：先讲清楚"存字典、`payment_id` 查重返回 `False` 而不是抛异常"这个设计选择的原
   因——重试是分布式系统里最常见的场景，接口应该对"重复提交同一个请求"宽容，而不是让调用方每次都要
   `try/except`。
3. **过渡到 Part 2 时**：主动列出退款可能失败的三种情况（时间戳格式错、payment 不存在、金额超额），
   并且现场说明"我打算用哪种异常类型区分它们"——`KeyError` vs `ValueError` 是一个值得展示"API 设计
   思考"的地方，不要三种情况都用一个笼统的 `Exception`。
4. **写部分退款累加时**：现场举一个"退两次刚好用完额度"和"退第二次超一分钱"的边界例子，证明自己想
   到了 `>` vs `>=` 的坑。
5. **Part 3 讲区间查询时**：主动说"现在是线性扫描，10^5 量级没问题；如果要支撑 10^7 级别的高频查
   询，我会按 `ts` 排序维护一个索引，用 `bisect` 定位区间边界"——即使不写代码，口头提到这一点也是加
   分项（对应追问②）。
6. **持久化**：解释为什么 `export_json` 必须连 `refund_ids` 集合一起序列化，而不是只存
   `refunded_cents` 累计值——因为幂等性依赖"这个 refund_id 是否已经处理过"，光有累计金额恢复不出这
   个信息。
7. **收尾**：跑一遍 worked examples 手算核对，再挑 1-2 条"面试官会怎么追问"（时区、并发写入竞态、
   审计日志）主动展开，呼应源材料里明确列出的 5 条追问方向。

## Open points
- The timestamp profile (`YYYY-MM-DDTHH:MM:SS`, naive, no offset) is this suite's own scoping
  decision to keep string-sort == chronological-sort trivially true and avoid aware/naive
  `datetime` comparison pitfalls. The timezone-aware variant is listed as a "Variants"/follow-up
  item (#4), not implemented.
- The exact command-stream protocol (`PAY`/`REFUND`/`REVENUE`/`RANGE` verbs, `OK`/`DUP`/`ERROR`
  tokens) is invented for this suite's io-test harness; programhelp.net's source describes only
  the class API, not a CLI protocol.

## Review（2026-09-02）
**改了什么**
- `test_cd02.py`：problem.md 的 worked examples 1–3 原来只被"拆散"覆盖（各测试用不同金额），没有逐字
  进测试（checklist F 项）。新增 `_example_ledger` / `_example2_ledger` 两个 helper 复现例子状态，加
  `test_example1_verbatim`（revenue 1500）、`test_example2_verbatim`（800 / r3 ValueError / r1 dup /
  ghost KeyError，且三次失败都不改状态）、`test_example3_verbatim`（区间查询 dict 逐字 + round-trip）。
  现在 24 tests：part1 6 · part2 6 · part3 12；edge 9 · fmt 1 · io 3 · perf 1。`IMPL=starter` 23
  failed / 1 passed（只有 `test_empty_stdin` 天然通过）。
- `solution.py` 重构为范本（公共 API 不变）：`Payment` dataclass 取代魔法字符串 key 的 dict
  （`p["amount"]`→`p.amount_cents`，字段名与 `get_payments_by_date` 的输出 dict 一致，`asdict` 直接
  出结果）；`net_cents` property 把"剩余可退额度"和"贡献的 revenue"收成一个定义，`add_refund` 的超额
  判断变成 `amount_cents > payment.net_cents`；`_parse_ts` 改为 `_validate_ts`（返回原串），
  `get_payments_by_date` 不再对每条记录 `strptime` 两次——固定宽度 profile 下已校验字符串的序 == 时间
  序，直接比字符串（这条本来就写在 REPORT 的 Open points 里，代码现在和说法一致；perf 测试 0.58 s）；
  命令流 harness 从一个 40 行 if/elif 改为 `COMMANDS` 分发表 + 每个动词一个 `_cmd_*` 函数，错误到文本
  的映射只在 harness 层，类本身不知道 CLI 协议；`PaymentLedger` / `__init__` / `get_total_revenue` /
  `export_json` / `load_json` 补一句话 docstring，类 docstring 列出两个状态字段及"为什么要持久化
  refund_ids"。
- `problem.md` Part 1："including the no-op duplicate path's own timestamp is still checked…"
  一句语法不通，改写为"the check runs before the duplicate check — an invalid timestamp on a
  duplicate call still raises `ValueError` rather than returning `False`"，语义不变。
- black 格式化 4 个文件（docstring 后空行等），`loop/lint.sh` 通过（flake8 原本就是 0）。
**为什么**：worked examples 逐字进测试与 lint 通过是 F 项；其余是 S 项（记录用 dataclass、规则表取代
散落 if、docstring、不重复解析）。4 个 worked examples 已用 `python3 solution.py` / 直接调类逐个核
对，输出逐字不变；`IMPL=starter` 失败集合与之前一致（多出的 3 个 example 测试也失败）。
**遗留**：无。`get_total_revenue` 保持 O(n) 求和而不维护 running total（避免第二份真相），O(1) 版本
与按 `ts` 的 bisect 索引仍只作为追问 #2/#6 口头讨论，不实现。
