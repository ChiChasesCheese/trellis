# cd02 · PaymentLedger — a small payment/refund bookkeeping class

**Type:** onsite coding / "Programming Exercise" (45 min, class-based, 3 parts) · **Stage:** 2026
Summer Intern Virtual Onsite, coding round · **Last asked:** 2026 (programhelp.net VO write-up,
undated within 2026) · **Frequency:** 1 direct source (programhelp.net, full method list + 5
follow-ups) · **Confidence:** medium-high — the method names, the idempotent-`payment_id` rule,
partial-refund support, and all 5 follow-up directions are directly from the source; the exact
signatures (parameter names/types), the timestamp format, the error contract (which failures
raise vs. return `False`), and the persistence methods are this problem.md's reconstruction to
make the source's one-paragraph description into something with pinned-down, testable behavior.

## Context
Stripe's internal tooling teams occasionally need a small, self-contained ledger object — no
database, no framework — that tracks payments and refunds for a single merchant and answers two
questions: "how much revenue do we actually have" and "what happened in this date range." This is
that object, built up in three interview-style stages.

## The class
```python
class PaymentLedger:
    def add_payment(self, payment_id: str, amount_cents: int, ts_iso: str, customer: str) -> bool: ...
    def add_refund(self, refund_id: str, payment_id: str, amount_cents: int, ts_iso: str) -> bool: ...
    def get_total_revenue(self) -> int: ...
    def get_payments_by_date(self, start_iso: str, end_iso: str) -> list[dict]: ...
    def export_json(self) -> str: ...
    @classmethod
    def load_json(cls, blob: str) -> "PaymentLedger": ...
```
All money is **integer cents**, never floats. All timestamps use one fixed profile:
`YYYY-MM-DDTHH:MM:SS` (naive — no `Z`, no UTC offset; see "Variants" for why). A timestamp that
doesn't match this shape, or that names a calendar-invalid date/time (`2026-02-30T00:00:00`,
`2026-01-01T25:00:00`), is invalid.

## Rules

### Part 1 — payments and revenue
`add_payment(payment_id, amount_cents, ts_iso, customer)`: records a new payment and returns
`True`. **If `payment_id` was already recorded, it is a no-op — return `False`** (an idempotent
retry, not an error); the original record is left untouched. `ts_iso` is validated on every call
and the check runs *before* the duplicate check — so an invalid timestamp on a duplicate call
still raises `ValueError` rather than returning `False`. `get_total_revenue()` returns the
sum of all recorded payment amounts (Part 1: no refunds exist yet, so this is a plain sum).

### Part 2 — partial refunds
`add_refund(refund_id, payment_id, amount_cents, ts_iso)`: applies a refund against an existing
payment and returns `True`. Rules, in order:
1. `ts_iso` is validated first (raises `ValueError` if malformed, before any other check).
2. **If `refund_id` was already applied, it is a no-op — return `False`** (same idempotent-retry
   contract as `add_payment`).
3. **If `payment_id` does not exist, raise `KeyError(payment_id)`** — this is a different failure
   mode from an idempotent duplicate; a refund against a payment that was never made is a caller
   bug, not a retry.
4. **If this refund would push cumulative refunds on that payment above the original
   `amount_cents`, raise `ValueError`.** Exact equality (refunding exactly the remaining balance)
   is allowed. Multiple partial refunds accumulate against the same running total.
`get_total_revenue()` becomes `sum(amount_cents) - sum(all successful refunds)` — a payment that
has been fully refunded contributes `0`, never negative.

### Part 3 — date-range query and persistence
`get_payments_by_date(start_iso, end_iso)`: both bounds **inclusive**. Validates both timestamps
first (raises `ValueError` on either being malformed — before touching any payment data). Returns
a `list[dict]`, one per matching payment, each shaped exactly:
```python
{"payment_id": str, "amount_cents": int, "ts": str, "customer": str, "refunded_cents": int}
```
sorted by **`ts` (chronological), then `payment_id` (plain string order)** as the tie-break.
`export_json() -> str` serializes the full ledger state (payments, their refund totals, and the
set of applied refund ids — needed so a reloaded ledger still rejects a duplicate refund replay).
`PaymentLedger.load_json(blob: str) -> PaymentLedger` is the inverse: a fresh ledger whose
`get_total_revenue()` and `get_payments_by_date(...)` are identical to the original's, and which
still enforces the same duplicate/over-refund rules on any further calls.

## Command-stream harness (for `main()` / io tests)
`main()` reads one command per line and prints one output line per command against a single
`PaymentLedger`:
```
PAY <payment_id> <amount_cents> <ts_iso> <customer>     -> PAY <payment_id> OK|DUP
REFUND <refund_id> <payment_id> <amount_cents> <ts_iso>  -> REFUND <refund_id> OK|DUP|ERROR <msg>
REVENUE                                                  -> REVENUE <cents>
RANGE <start_iso> <end_iso>                              -> RANGE <count>
                                                             <payment_id> <amount_cents> <ts> <customer> <refunded_cents>
                                                             ... (count lines, same sort as get_payments_by_date)
```
`customer` is a single whitespace-free token (e.g. `cus_a1b2`), never a display name with spaces.
A malformed `PAY` timestamp prints `PAY <payment_id> ERROR <message>` instead of `OK`/`DUP`; a
malformed `RANGE` bound prints `RANGE ERROR <message>` with no following rows.

## Worked examples
All verified by running `solution.py`.

### Example 1 (Part 1)
```python
L = PaymentLedger()
L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")  # -> True
L.add_payment("p2", 500,  "2026-01-02T09:00:00", "cus_b")  # -> True
L.add_payment("p1", 999,  "2026-01-03T00:00:00", "cus_a")  # -> False (duplicate id, ignored)
L.get_total_revenue()                                       # -> 1500
```

### Example 2 (Part 2)
```python
L.add_refund("r1", "p1", 300, "2026-01-05T00:00:00")  # -> True  (300 <= 1000)
L.add_refund("r2", "p1", 400, "2026-01-06T00:00:00")  # -> True  (300+400=700 <= 1000)
L.get_total_revenue()                                  # -> 1500 - 700 = 800
L.add_refund("r3", "p1", 400, "2026-01-07T00:00:00")  # -> raises ValueError (700+400=1100 > 1000)
L.add_refund("r1", "p1", 300, "2026-01-08T00:00:00")  # -> False (r1 already applied)
L.add_refund("rX", "ghost", 100, "2026-01-08T00:00:00")  # -> raises KeyError('ghost')
```

### Example 3 (Part 3)
```python
L.get_payments_by_date("2026-01-01T00:00:00", "2026-01-02T23:59:59")
# -> [
#      {"payment_id": "p1", "amount_cents": 1000, "ts": "2026-01-01T10:00:00", "customer": "cus_a", "refunded_cents": 700},
#      {"payment_id": "p2", "amount_cents": 500,  "ts": "2026-01-02T09:00:00", "customer": "cus_b", "refunded_cents": 0},
#    ]
blob = L.export_json()
L2 = PaymentLedger.load_json(blob)
L2.get_total_revenue() == L.get_total_revenue()          # -> True
L2.get_payments_by_date(...) == L.get_payments_by_date(...)  # -> True
```

### Example 4 (command stream)
```
PAY p1 1000 2026-01-01T10:00:00 cus_a
PAY p2 500 2026-01-02T09:00:00 cus_b
PAY p1 999 2026-01-03T00:00:00 cus_a
REFUND r1 p1 300 2026-01-05T00:00:00
REVENUE
RANGE 2026-01-01T00:00:00 2026-01-02T23:59:59
```
```
PAY p1 OK
PAY p2 OK
PAY p1 DUP
REFUND r1 OK
REVENUE 1200
RANGE 2
p1 1000 2026-01-01T10:00:00 cus_a 300
p2 500 2026-01-02T09:00:00 cus_b 0
```

## Edge cases hidden tests are known to target
- duplicate `payment_id` returns `False` and does **not** overwrite amount/ts/customer.
- refunding **exactly** the remaining balance is allowed (boundary: `refunded + amount ==
  amount_cents`), one cent over raises `ValueError`.
- two (or more) partial refunds against the same payment accumulate correctly toward the cap.
- duplicate `refund_id` is idempotent (`False`), even when the payment could technically still
  absorb more refund — the dedup check happens before the amount check.
- refund against a payment id that was never added: `KeyError`, distinguishable from the
  idempotent-duplicate `False` path.
- `get_total_revenue()` on an empty ledger is `0`; a fully-refunded payment contributes `0`, not
  negative.
- `get_payments_by_date` boundaries are inclusive on both ends; a payment timestamped exactly on
  `start_iso` or `end_iso` is included; one second outside either bound is excluded.
- invalid timestamp shapes: missing `T` separator (`2026-01-01 00:00:00`), calendar-invalid date
  (`2026-02-30T00:00:00`), calendar-invalid time (`2026-01-01T25:00:00`), and a non-string value
  are all `ValueError` — each raised at every entry point that accepts a timestamp
  (`add_payment`, `add_refund`, `get_payments_by_date`).
- `export_json`/`load_json` round-trip preserves refund totals *and* the set of applied
  `refund_id`s — a `load_json`-reconstructed ledger still rejects a replayed duplicate refund and
  still enforces the over-refund cap correctly.
- large ledger: 10^5 payments, a `get_payments_by_date` query over a narrow window — must not be
  quadratic in the number of queries against ledger size.

## Variants seen in the wild
- programhelp.net's own follow-up list (see Sources) surfaces five extension directions, folded
  into "面试官会怎么追问" below rather than treated as base requirements: partial-refund edge cases
  (covered here as Part 2 core, not a follow-up), query-at-scale optimization, invalid-timestamp
  handling (covered here as a core `ValueError` contract, not a follow-up), range queries (Part 3
  core), and persistence to a real database (this problem.md substitutes `export_json`/`load_json`
  as the in-memory analogue of that follow-up, since a real DB integration isn't testable offline).
- Timezone-aware variant: `ts_iso` carries a UTC offset or `Z` suffix; comparisons must normalize
  to a common zone before ordering (not implemented here — naive timestamps only; see "面试官会怎么
  追问" #4).
- A stricter variant validates `amount_cents >= 0` and rejects negative amounts outright (not
  enforced here — zero-amount payments/refunds are valid edge cases, negative amounts are
  out-of-scope/undefined for this version).

## What this tests
skills: S02 parsing/validation with a fixed timestamp profile · S03 an incrementally-revealed
class API rather than free functions · S06 integer-cents money, never float-accumulate · S08
deterministic multi-key sort · S09 exact command-stream output formatting · S17 error-contract
design (idempotent no-op vs. `KeyError` vs. `ValueError` — three distinct failure shapes for three
distinct situations) · S18 validation and defensive input handling · S20 serialization round-trip
correctness

## Sources
- `loop/raw/cn_forums.md` line 104: "programhelp.net《Stripe 2026 Summer Intern VO》Coding 轮
  （45 分钟）：设计一个轻量级支付交易记录系统，实现 `PaymentLedger` 类：`Add_payment()`、
  `Add_refund()`、`Get_total_revenue()`、`Get_payments_by_date()`；需按 `payment_id` 防重复记录；
  支持部分退款（扣减金额）。追问包括：①处理部分退款金额小于原支付的情况 ②海量数据场景下的查询优
  化 ③非法时间戳格式的错误处理 ④按时间范围查询（如取某月数据）⑤数据持久化到数据库。评估重点：
  面向对象设计、边界处理、代码清晰度、可扩展性、权衡意识——不是复杂算法。"
  [programhelp.net/en/vo/stripe-intern-vo-coding-integration/]

## 面试官会怎么追问
1. 上面第①条追问原文是"处理部分退款金额**小于**原支付的情况"——这其实已经是本题 Part 2 的核心规则
   （累计退款 ≤ 原金额），面试现场如果你先只实现了"退一次全额退款"，这就是面试官会追的第一个问题：
   "如果客户只想退一部分钱呢？如果退两次呢？"
2. 第②条"海量数据场景下的查询优化"：现在 `get_payments_by_date` 是线性扫描全部 payment。如果要支
   持 10^7 笔记录上的高频区间查询，你会怎么维护一个按 `ts` 排序的索引（比如 `bisect` 二分定位区
   间边界，或者按天分桶）？插入新 payment 时索引怎么增量维护，而不是每次查询都重新排序一遍？
3. 第③条"非法时间戳格式的错误处理"：现在只有一种严格格式 `YYYY-MM-DDTHH:MM:SS` 会被接受。如果上游
   系统会同时发来"2026-01-01"（无时间部分）、Unix 时间戳（整数秒）、甚至字符串"null"这三种格式混
   杂的历史数据，你的校验/解析层要怎么演进成"尽量兼容、明确拒绝"而不是"越写越多 if"？
4. 时区：现在假设所有时间戳都是同一个隐含时区的 naive 时间。如果 `ts_iso` 可能带 UTC 偏移
   （`+08:00`）或者 `Z` 后缀，你的区间比较逻辑要怎么改？两个不同时区的时间戳能直接按字符串排序吗
   （不能——这是一个常见陷阱，值得主动指出）？
5. 第⑤条"数据持久化到数据库"：`export_json`/`load_json` 只是内存态的序列化。如果换成真的 SQL 数
   据库，`add_payment`/`add_refund` 的"先校验后写入"逻辑要怎么变成事务？两个并发请求同时对同一笔
   `payment_id` 调用 `add_payment` 会不会产生竞态（都读到"不存在"然后都写入）？你会用什么手段防止
   （唯一约束 + 捕获冲突异常，而不是先查后写）？
6. 审计：如果央行/监管要求每一次退款操作都有不可篡改的审计记录（谁在什么时候退了多少钱、退款前后
   余额各是多少），你现在的 `_payments` 字典只保留"最终状态"（`refunded` 累计值），要怎么改成同时
   保留每一笔退款事件的完整历史，而不影响 `get_total_revenue()` 的 O(1) 均摊读取？
