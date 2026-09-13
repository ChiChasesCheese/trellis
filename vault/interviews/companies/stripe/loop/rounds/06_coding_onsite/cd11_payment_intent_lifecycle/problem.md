# cd11 · PaymentIntent lifecycle — a small state-machine class (init → change → fail → time)

**Type:** onsite coding / "Programming Exercise" (class-based, 4 parts) · **Stage:** onsite,
technical coding round (reconstructed target) · **Confidence（置信度）：low** — see 警示块 below.

> ⚠️ **四个上游文件只有标题和摘要，正文在付费墙后，本仓库读不到**：`catalog/raw/mirror_1p3a_stripe/coding/`
> 下的四个 `.txt` 文件（`146…part_1_initializing_the_system`、`145…part_2_change_is_good`、
> `149…part_3_accepting_failure`、`148…part_4_timing_matters`，均标注 `Source Type: OJ / More
> Problems`，摘要块自称 "Question Summary" 而不是原题面）指向：
> - https://www.1point3acres.com/interview/problems/ef09d8a4-9852-499b-98ab-1c9887bd9b33 (Part 1)
> - https://www.1point3acres.com/interview/problems/3adeb37a-4f02-4b97-8eba-979e94169e19 (Part 2)
> - https://www.1point3acres.com/interview/problems/33ee3a0c-500b-4bf0-8163-53dd208e7dfe (Part 3)
> - https://www.1point3acres.com/interview/problems/0644b8b3-d726-43a7-ad22-cd87ca1c7f62 (Part 4)
>
> 四个 URL 本轮均未直接抓取（一亩三分地正文在付费墙后，镜像文件本身也只存了标题 + 3-5 句摘要，
> 没有正文、没有函数签名、没有样例）。**能从上游拿到、且本题据此保留的信息只有两条：**
> (1) 这是同一道题的四个 part，标题分别是 "Initializing the System" / "Change is Good!" /
> "Accepting Failure" / "Timing Matters"，暗示"建立初始状态 → 状态变更 → 失败路径 → 时间维度"
> 的递进顺序；(2) 摘要里明确提到的关键词——"Payment Intent"、"merchant"、"state machine"、
> "REQUIRES_ACTION/PROCESSING/COMPLETED" 这几个状态名、"UPDATE 命令改金额且仅在
> REQUIRES_ACTION 生效"、"FAIL 仅在 PROCESSING 生效"、"REFUND 仅在 COMPLETED 且未退款过时生效"、
> "part 4 是带时间戳的商户级退款超时窗口策略"。**这几条摘要内容和本仓库已有的
> `problems/q10_payment_intent_commands`（其五个来源里明确包含这四个标题里的三个之一被引用的
> "REFUND + window" version C）高度重合**——换句话说，上游摘要描述的规则集，本仓库已经用 q10
> 精确建模过了。
>
> 因此本题**故意不复用 q10 的规则集**：状态名、命令名、UPDATE/FAIL/REFUND 的具体触发条件、
> part 4 的时间窗口机制，下面全部是本仓库重新设计的一套**不同但同样贴合四个标题**的规则
> （改用真实 Stripe `requires_payment_method`/`processing`/`succeeded`/`canceled` 状态名、
> card vs. bank_debit 两种支付方式分叉、confirm 次数过多自动 `canceled`、按 `settle_window`
> 判定的到期/取消窗口——这些细节来自 `loop/study/20-cards/stripe_api.md`「PaymentIntent 状态机」
> 一节，即公开的 Stripe 官方文档转述，不是编的）。**只有四个 part 的数量、顺序、主题**
> （建立初始状态 → 状态变更 → 失败路径 → 时间维度）算是有上游依据；**规则细节、输入输出格式、
> 全部样例都是本仓库自拟**，不代表任何人转述过的真实面试规格。做这道题是为了练"class 设计 +
> 官方状态机细节"，不是为了背题。See `REPORT.md` §与 q10 的区别 for exactly which rules diverge
> and why the two problems must not be studied as if they share one rule set.

## Context
A Stripe **PaymentIntent** tracks one payment through its lifecycle. Unlike `q10`'s simplified
three-state OA machine, this onsite version distinguishes **synchronous** payment methods
(`card`: confirming decides success or failure immediately) from **asynchronous** ones
(`bank_debit`: confirming only starts processing; the outcome — settle or fail — arrives later,
and is itself time-bounded). Money only moves into a merchant's balance once a PaymentIntent
reaches `succeeded`. This is an onsite ("VO") round: **you are expected to design a class**, not
just a `part(lines) -> list[str]` pipeline — see `PaymentIntentEngine` below.

## The class
```python
class PaymentIntentEngine:
    def __init__(self, max_confirm_attempts: int = 3) -> None: ...
    def init_merchant(self, merchant_id: str, balance_cents: int) -> bool: ...
    def create_intent(self, intent_id: str, merchant_id: str, amount_cents: int, method: str,
                       settle_window: int | None = None) -> bool: ...
    def confirm(self, intent_id: str, ts: int | None = None) -> str: ...
    def settle(self, intent_id: str, ts: int | None = None) -> bool: ...
    def fail(self, intent_id: str, ts: int | None = None) -> bool: ...
    def cancel(self, intent_id: str, ts: int | None = None) -> bool: ...
    def expire(self, intent_id: str, ts: int) -> bool: ...
    def update_amount(self, intent_id: str, amount_cents: int) -> bool: ...
    def change_method(self, intent_id: str, method: str) -> bool: ...
    def get_status(self, intent_id: str) -> str | None: ...
    def get_balance(self, merchant_id: str) -> int | None: ...
    def balances(self) -> list[tuple[str, int]]: ...
```
`method ∈ {"card", "bank_debit"}`. Status strings are the real Stripe names:
`"requires_payment_method"` (initial) → `"processing"` (async only) → `"succeeded"`, or
→ `"canceled"` (terminal, from either of the first two states). Money is always integer cents.

## Rules

### Part 1 — Initializing the System
- `init_merchant(m, balance)`: create merchant `m`. **If `m` already exists, ignored** (`False`,
  balance untouched). Balance may be negative or 0.
- `create_intent(id, m, amount, method, settle_window=None)`: create a PaymentIntent in
  `requires_payment_method`. Ignored (`False`) if: `id` already exists; `m` is unknown;
  `amount < 0` (0 is allowed); `method` is not `"card"`/`"bank_debit"`. (`settle_window` is
  unused — always pass/accept `None` — until Part 4; see there for its own validation.)
- `confirm(id, ts=None)`: only acts when the intent is `requires_payment_method`; otherwise
  returns `"ignored"` (no state change). On success it always increments the intent's internal
  confirm-attempt counter and records `ts` as `confirmed_at` (both only *matter* from Part 3 /
  Part 4 onward). Then:
  - `method == "card"` (**synchronous**): the intent moves straight to `"succeeded"` and
    **`balance[m] += amount` happens right now** — returns `"succeeded"`.
  - `method == "bank_debit"` (**asynchronous**): the intent moves to `"processing"` — no balance
    change yet — returns `"processing"`.
- `settle(id, ts=None)`: only acts when the intent is `"processing"` — moves it to `"succeeded"`
  and **now** credits `balance[m] += amount` (the amount at settlement time, see Part 2). Any
  other state (including calling it on a `card` intent, which never reaches `"processing"` in
  Part 1–3) → ignored, `False`.
- `balances()`: `[(merchant_id, balance_cents), ...]` for every merchant ever `init_merchant`ed,
  sorted by `merchant_id` in plain string order. A merchant with balance 0 is still listed.

### Part 2 — Change Is Good!
- `update_amount(id, amount)`: sets the amount **only while the intent is
  `requires_payment_method`**; ignored in `processing`/`succeeded`/`canceled`, for an unknown
  `id`, or when `amount < 0` (0 is allowed). A later `confirm`/`settle` credits the *updated*
  amount, not the amount at `create_intent` time.
- `change_method(id, method)`: swaps `card` ⇄ `bank_debit` **only while
  `requires_payment_method`**; ignored otherwise, and ignored for an invalid `method` string.
  Because Part 1's `confirm` branches on `method` at confirm time, switching `bank_debit → card`
  before confirming turns a would-be `processing` payment into an immediate `succeeded` one, and
  vice versa — this is the whole point of "change is good": the merchant's future, not just the
  amount, can still be reshaped up until the customer actually confirms.

### Part 3 — Accepting Failure
- `fail(id, ts=None)`: only acts when the intent is `"processing"` — moves it **back to
  `"requires_payment_method"`** so it can be `update_amount`d / `change_method`d / `confirm`ed
  again. This is the real Stripe behavior (`loop/study/20-cards/stripe_api.md` §PaymentIntent
  状态机: "支付被拒之后状态退回 requires_payment_method 以便重试") and the detail this problem
  most wants you to get right — **not** a transition to some new "failed" state, and **not** the
  same target state as `q10`'s `FAIL` (which goes `PROCESSING → REQUIRES_ACTION`, a state this
  problem doesn't have at all). Crucially, `fail` does **not** reset the confirm-attempt counter
  — see the next bullet.
- **Auto-cancel after too many confirms** (no dedicated command — this lives inside `confirm`
  itself, starting now that `fail` exists to make repeat confirms possible): each time `confirm`
  is about to act on an intent in `requires_payment_method`, it increments that intent's
  confirm-attempt counter *first*. If the counter now exceeds `max_confirm_attempts` (constructor
  default `3` — i.e. the intent has already been confirmed 3 times), this 4th call does **not**
  process the payment at all: the intent moves straight to `"canceled"` and `confirm` returns
  `"canceled"`. This models Stripe's real anti-abuse behavior
  (`stripe_api.md`: "被 confirm 的次数过多"会被系统自动 `canceled`") — it is about the *number of
  confirm attempts*, not the number of failures, though in this model the only way to rack up
  more than one confirm attempt on the same intent is via `fail` sending it back to
  `requires_payment_method`, since a synchronous `card` confirm is terminal on the first try.
- `cancel(id, ts=None)`: manual cancellation.
  - `requires_payment_method` → `"canceled"`, **always** allowed.
  - `"processing"` → `"canceled"` **only if `method == "bank_debit"`** (an async payment can be
    pulled back before it lands; a `card` intent is never `"processing"` in this model, so this
    branch is bank_debit-only in practice, but the rule is method-based, not method-specific by
    accident — Part 4 adds a time window on top of this same branch).
  - `"succeeded"` or already `"canceled"` → ignored, `False` (terminal states).

### Part 4 — Timing Matters
Every command now carries an integer timestamp `t` (see Input format). `confirmed_at` (set by
`confirm`) and `t` are compared directly — timestamps are otherwise opaque integers, not
calendar dates.
- `create_intent(..., settle_window=...)` gains real meaning:
  - `settle_window=None` (absent on the command line): **no time limit** — `settle`/`fail`/a
    processing-time `cancel` are allowed at any later timestamp.
  - `settle_window=0`: **zero grace** — `settle`/`fail`/a processing-time `cancel` are allowed
    **only at the exact same timestamp as the confirm** (`t == confirmed_at`); one tick later is
    too late. (This is deliberately *not* the same meaning as `q10`'s `refund_limit=0`, which
    forbids the action outright forever — here `0` still allows the same-tick case.)
  - `settle_window < 0`: **the whole `create_intent` call is rejected** (`False`, no intent is
    created at all) — this is deliberately *not* the same as `q10`'s negative-refund-limit rule
    (which coerces a negative limit into "unlimited"); here a negative window is treated as a
    malformed argument, not a permissive default.
- `settle(id, ts)` / `fail(id, ts)`: in addition to the Part 1/3 state check, require
  `settle_window is None or (ts - confirmed_at) <= settle_window`; otherwise ignored (the intent
  is left stuck in `"processing"` — nothing auto-resolves it except `expire`, below).
- `cancel(id, ts)`: the `requires_payment_method` branch is **unaffected by timing** (always
  allowed, exactly as Part 3). The `processing` + `bank_debit` branch additionally requires the
  same window check as `settle`/`fail`.
- `expire(id, ts) -> bool` (**new in Part 4**): the system reaping a stuck payment. Acts only if
  the intent is `"processing"` **and** `settle_window is not None` **and**
  `(ts - confirmed_at) > settle_window` — then moves it to `"canceled"` and returns `True`.
  Otherwise a no-op (`False`) — in particular, an intent created with `settle_window=None` never
  expires no matter how late `ts` is; it must be resolved manually via `settle`/`fail`/`cancel`.

## Input (stdin, for `main()` / `partN(lines)` / io tests)
First line `PART n` (`n` ∈ 1..4; missing header defaults to `PART 4`, the full rule set — a
strict superset of 1–3). Remaining lines, one command each, whitespace-separated, blank lines
ignored. **Parts 1–3 commands carry no timestamp; every Part 4 command is prefixed with an
integer `t`** (non-negative, non-decreasing across the file, though only `confirm`'s recorded
`ts` and the later comparison against it are semantically load-bearing — the values on
non-timing commands like `INIT`/`CREATE`/`UPDATE`/`CHANGE_METHOD`/`BALANCE` are consumed for
uniform parsing only). A command word not yet unlocked by the selected part (or any malformed
line: wrong argument count, non-integer number, unknown `method`) is skipped — no output line
for it, and no effect. Up to 2×10⁵ lines.

```
INIT <merchant> <balance>
CREATE <id> <merchant> <amount> <method>            (Part 4: + optional trailing [settle_window])
CONFIRM <id>
SETTLE <id>
UPDATE <id> <amount>                                 (Part 2+)
CHANGE_METHOD <id> <method>                          (Part 2+)
FAIL <id>                                            (Part 3+)
CANCEL <id>                                          (Part 3+)
EXPIRE <id>                                          (Part 4 only)
BALANCE <merchant>
```
In Part 4, every line above is `<t> <command ...>` instead.

## Output
One line per command that produces a result, in the exact shapes below (`INIT` produces no
output line at all):
```
CREATE <id> OK|IGNORED
CONFIRM <id> succeeded|processing|canceled|ignored
SETTLE <id> OK|IGNORED
FAIL <id> OK|IGNORED
CANCEL <id> OK|IGNORED
EXPIRE <id> OK|IGNORED
UPDATE <id> OK|IGNORED
CHANGE_METHOD <id> OK|IGNORED
BALANCE <merchant> <amount>|UNKNOWN
```
`CONFIRM`'s third token is **exactly the string `confirm()` returns** (lowercase, one of the four
listed) — it is not the same vocabulary as the uppercase `OK`/`IGNORED` used by every other
command; do not conflate the two. No output at all for zero commands.

## Worked examples
All verified by running `solution.py`.

### Example 1 (Part 1 — card vs. bank_debit)
```
PART 1
INIT m1 0
CREATE p1 m1 100 card
CONFIRM p1
CREATE p2 m1 50 bank_debit
CONFIRM p2
SETTLE p2
BALANCE m1
```
```
CREATE p1 OK
CONFIRM p1 succeeded
CREATE p2 OK
CONFIRM p2 processing
SETTLE p2 OK
BALANCE m1 150
```
(`p1` is `card`: confirming credits the balance immediately. `p2` is `bank_debit`: confirming
only starts `processing`; `settle` is the event that actually credits it. `100 + 50 = 150`.)

### Example 2 (Part 2 — proration-free "change": amount and method both reshape the outcome)
```
PART 2
INIT m1 0
CREATE p1 m1 100 card
UPDATE p1 80
CHANGE_METHOD p1 bank_debit
CONFIRM p1
SETTLE p1
UPDATE p1 999
BALANCE m1
```
```
CREATE p1 OK
UPDATE p1 OK
CHANGE_METHOD p1 OK
CONFIRM p1 processing
SETTLE p1 OK
UPDATE p1 IGNORED
BALANCE m1 80
```
(`p1` was created as a `card` payment for 100, then changed to amount 80 **and** method
`bank_debit` before ever confirming — so `confirm` now takes the async branch, `settle` credits
the *updated* 80, and the final `UPDATE` is ignored because the intent is already `succeeded`.)

### Example 3 (Part 3 — retry after failure, auto-cancel after too many confirms, manual cancel)
```
PART 3
INIT m1 0
CREATE p1 m1 100 bank_debit
CONFIRM p1
FAIL p1
CONFIRM p1
FAIL p1
CONFIRM p1
FAIL p1
CONFIRM p1
CREATE p2 m1 40 card
CANCEL p2
CREATE p3 m1 20 bank_debit
CONFIRM p3
CANCEL p3
BALANCE m1
```
```
CREATE p1 OK
CONFIRM p1 processing
FAIL p1 OK
CONFIRM p1 processing
FAIL p1 OK
CONFIRM p1 processing
FAIL p1 OK
CONFIRM p1 canceled
CREATE p2 OK
CANCEL p2 OK
CREATE p3 OK
CONFIRM p3 processing
CANCEL p3 OK
BALANCE m1 0
```
(`p1` is confirmed and failed three times — each `fail` sends it back to
`requires_payment_method` for a retry, exactly as `stripe_api.md` describes. Its 4th `confirm`
call pushes the attempt counter to 4, over the default `max_confirm_attempts=3`, so it
auto-`canceled` instead of processing a fourth time. `p2` (`card`, still
`requires_payment_method`) is cancelled manually with no restriction. `p3` (`bank_debit`) is
cancelled while `"processing"` — allowed because its method is async. None of the three ever
reached `succeeded`, so `m1`'s balance is untouched at `0`.)

### Example 4 (Part 4 — settle window, zero-grace, expire, a rejected negative window)
```
PART 4
1 INIT m1 0
2 CREATE p1 m1 100 bank_debit 5
3 CONFIRM p1
8 SETTLE p1
2 CREATE p2 m1 50 bank_debit 5
3 CONFIRM p2
20 EXPIRE p2
2 CREATE p3 m1 30 bank_debit 0
3 CONFIRM p3
3 SETTLE p3
2 CREATE p4 m1 10 bank_debit -1
3 CONFIRM p4
20 BALANCE m1
```
```
CREATE p1 OK
CONFIRM p1 processing
SETTLE p1 OK
CREATE p2 OK
CONFIRM p2 processing
EXPIRE p2 OK
CREATE p3 OK
CONFIRM p3 processing
SETTLE p3 OK
CREATE p4 IGNORED
CONFIRM p4 ignored
BALANCE m1 130
```
(`p1`: `settle_window=5`, confirmed at `t=3`; `SETTLE` at `t=8` is exactly on the boundary
(`8−3=5 ≤ 5`) → succeeds, credits 100. `p2`: same window, never settled/failed; at `t=20` it is
`17` ticks past confirm, over the window, so `EXPIRE` succeeds and cancels it — no credit. `p3`:
`settle_window=0` (zero grace, not "never"), confirmed and settled at the **same** `t=3` →
`0 ≤ 0` → succeeds, credits 30. `p4`: `settle_window=-1` is a malformed argument, so the whole
`CREATE` is rejected — `p4` never exists, so its `CONFIRM` is `ignored`. Total: `100 + 0 + 30 =
130`.)

## Edge cases hidden tests are known to target
- second `init_merchant` for the same id does not reset the balance.
- `create_intent` with a duplicate id, unknown merchant, negative amount, or invalid `method` →
  ignored; amount `0` is valid.
- `confirm` on `processing`/`succeeded`/`canceled`/unknown id → `"ignored"`, no state change, no
  attempt-counter increment.
- `settle`/`fail` on anything but `"processing"` → ignored; calling `settle` on a `card` intent
  (which is never `"processing"`) is always ignored, not an error.
- `update_amount`/`change_method` after `confirm` (i.e. once `processing` or `succeeded`) are
  ignored — but after a `fail` sends the intent back to `requires_payment_method`, both apply
  again, and the eventual `settle`/immediate-`confirm` credits the *latest* amount/method.
  Two consecutive `change_method` calls before ever confirming both apply (last one wins).
- the confirm-attempt counter is **not** reset by `fail`; exactly `max_confirm_attempts` (3 by
  default) confirms succeed in processing the payment (whether they end in `processing` or
  `succeeded`), and the very next one auto-cancels — off-by-one here (`>` vs `>=` against
  `max_confirm_attempts`) is the classic bug.
- `cancel` on `"processing"` for a `card`-method intent (not reachable through normal `confirm`
  flow, but reachable if `change_method` swaps it back to `card` — no: `change_method` only
  applies in `requires_payment_method`, so a `card` intent is provably never `"processing"`; a
  hidden test may still call `cancel`/`settle`/`fail` on a hand-constructed engine state or via
  `PaymentIntentEngine.__init__` internals to confirm this is enforced by the method check, not
  merely "happens to never occur").
- `cancel` on `"succeeded"` or already-`"canceled"` → ignored (idempotent — a second `cancel` is
  a no-op), whether reached manually or via `expire`/auto-cancel-by-attempts.
- Part 4 window boundary: `ts − confirmed_at == settle_window` is allowed for `settle`/`fail`/
  processing-`cancel`; `settle_window + 1` is refused (stays `"processing"`, retryable at a
  later, still-in-window timestamp were one to exist — but note the ticks are non-decreasing, so
  a refused `settle` cannot itself be "retried earlier").
  a `settle_window` of `0` allows exactly `ts == confirmed_at`, refuses `ts == confirmed_at + 1`.
- `settle_window=None` (omitted) never triggers `expire`, no matter how large `ts` grows.
- a negative `settle_window` makes `create_intent` return `False` outright — no intent, no
  merchant-balance side effect, and every subsequent command referencing that id is `ignored`.
- `expire` on a `requires_payment_method`/`succeeded`/`canceled` intent, or on one whose window
  hasn't elapsed yet, is a no-op — it never fires "early."
- merchants with balance 0 are still listed by `balances()`/`BALANCE`; sort order is plain string
  order (`"m10" < "m2"`).
- unknown command words, wrong argument counts, and non-integer numbers are skipped without
  crashing and without an output line.

## Variants seen in the wild
- The upstream titles ("Initializing the System" / "Change Is Good!" / "Accepting Failure" /
  "Timing Matters") and the summary's mention of `REQUIRES_ACTION`/`PROCESSING`/`COMPLETED` state
  names, an `UPDATE`-only-in-`REQUIRES_ACTION` rule, a `FAIL: PROCESSING → REQUIRES_ACTION` rule,
  and a `REFUND`-once-when-`COMPLETED` rule, describe essentially the same command language this
  repo has already modeled precisely as `problems/q10_payment_intent_commands` (an OA, not an
  onsite round) — see that problem's own Sources for the independently-corroborated version of
  those exact rules. **This problem deliberately does not reuse that rule set** — see
  `REPORT.md` §与 q10 的区别.
- A from-scratch reconstruction of a class-based onsite round in this domain could equally well
  choose to expose `REFUND` instead of / in addition to `cancel`+`expire` for Part 4's timing
  angle (a per-merchant refund window, as `q10` Part 4 does) — this problem.md picks the
  async-settlement-window + auto-cancel-by-attempts angle instead specifically to avoid
  duplicating q10's tested surface; both are equally plausible readings of a two-word title like
  "Timing Matters".

## What this tests
skills: S01 reading a multi-part spec and designing for Part N+1 from the start · S02 line
parsing with a variable timestamp prefix · S03 modelling the domain as a class
(`PaymentIntentEngine`) plus small records, not a bag of dicts — the VO-vs-OA differentiator ·
S10 state machines with a genuine reversal path (`processing → requires_payment_method`) · S11
idempotency (duplicate `init_merchant`/`create_intent`, repeated `cancel`) · S12 time windows
measured from an event timestamp recorded mid-lifecycle (`confirmed_at`), not from creation · S17
error/no-op contract design (`bool` vs. a four-way status string for `confirm` specifically) ·
S18 validation and defensive input handling (a malformed `settle_window` rejects the whole
command, not just the field) · S19 incremental design across 4 parts on one persistent object ·
S24 domain literacy (Stripe's real `requires_payment_method`/`processing` names and its two
documented failure/timeout behaviors from `stripe_api.md`).

## Sources
- `catalog/raw/mirror_1p3a_stripe/coding/146__20250304__for_all_intents_and_purposes_part_1_initializing_the_system__oj_ef09d8a4.txt`
- `catalog/raw/mirror_1p3a_stripe/coding/145__20250304__for_all_intents_and_purposes_part_2_change_is_good__oj_3adeb37a.txt`
- `catalog/raw/mirror_1p3a_stripe/coding/149__20250304__for_all_intents_and_purposes_part_3_accepting_failure__oj_33ee3a0c.txt`
- `catalog/raw/mirror_1p3a_stripe/coding/148__20250304__for_all_intents_and_purposes_part_4_timing_matters__oj_0644b8b3.txt`
  (all four: title + "Question Summary" bullet list only; the underlying 1point3acres URLs above
  are behind a paywall this repo could not read — see 警示块.)
- `loop/study/20-cards/stripe_api.md` §PaymentIntent 状态机 (Stripe's public lifecycle docs,
  transcribed) — source of the real state names, the "declined → back to
  `requires_payment_method`" rule, and the "auto-`canceled` after too many confirms" rule used
  here.
- `problems/q10_payment_intent_commands/problem.md` — the sibling OA problem this onsite problem
  deliberately does not duplicate; see that file's own Sources for the independently-corroborated
  command language this problem's rules diverge from.
