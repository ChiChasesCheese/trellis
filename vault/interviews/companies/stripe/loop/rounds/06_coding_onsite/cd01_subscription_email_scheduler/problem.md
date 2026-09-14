# cd01 · Subscription email scheduler

**Type:** onsite coding / "Programming Exercise" (60 min, 3 parts) · **Stage:** onsite, technical
coding round · **Last asked:** 2025-12-08 (linkjob intern transcript; recurring theme through 2026)
**Frequency:** cross-referenced across 3 independent sources (linkjob intern 2025, linkjob "2026
Java NG VO — Email Subscription" 2025-12-08, Simplify 2026 summary) plus a fourth, differently-worded
1point3acres entry (「Subscription Email Scheduler」, 3-step TOC) · **Confidence:** medium — the
3-part shape (schedule basics → plan changes → renewals) and the domain (subscription lifecycle
emails) are corroborated by four independent write-ups, but none publishes exact field names or
output formatting; this problem.md is this suite's own concrete reconstruction. **It intentionally
uses different fields/actions/output format than `problems/q07_subscription_notifications`
(day-offsets, `[Changed]`/`[Renewed]` tags)** — this is the calendar-date, single-verb-per-line
"VO" variant of the same theme family; do not conflate the two rule sets.

## Context
A subscription product sends three kinds of lifecycle emails: a `welcome` when a subscription
starts, an `expiring` warning shortly before it ends, and an `expired` notice when it ends.
Customers can also change plans mid-term, renew before their term is up, or cancel outright. You
are given a stream of subscription events and must print the exact set of emails the system would
send within a requested date window.

## Input (stdin)
First line `PART n` (`n ∈ {1,2,3}`; missing header defaults to the full Part 3 rule set — it is a
strict superset). Remaining lines, in any order:

* **Event line**: `date,user,action[,plan]` — `date` is `YYYY-MM-DD`. `action ∈ {subscribe,
  change, renew, cancel}`. `subscribe` and `change` carry a fourth field `plan ∈ {monthly,
  annual}`; `renew` and `cancel` have no fourth field (renewing keeps the current plan).
* **Query line** (always the *last* non-blank line): `FROM..TO`, two `YYYY-MM-DD` dates joined by
  `..`, no spaces. Inclusive on both ends. If the last non-blank line does not match this shape,
  no window is applied (equivalent to an unbounded range) — used by a few tests below that only
  care about the schedule, not filtering.

Events are **not guaranteed to be in date order** in the file; they are always processed in
`(date, input line order)`, never file order. Blank lines are ignored; spaces around commas are
tolerated. Up to 10^5 event lines.

## Output
One line per email that falls inside `[FROM, TO]`: `date user email_type`
(`email_type ∈ {welcome, expiring, expired, renewed, canceled}`). Sorted by **`date`, then `user`
(plain string order), then a fixed email-type priority — `welcome`(0) < `expiring`(1) <
`expired`(2) < `renewed`(3) < `canceled`(4) — never by the order events were processed.** Nothing
is printed for an empty schedule.

## Rules

### Part 1 — scheduling basics
Only `subscribe` events are honored; `change`/`renew`/`cancel` lines are parsed but ignored
entirely (no effect, no output) in Part 1. `period_days(monthly) = 30`, `period_days(annual) =
365`. For `date,user,subscribe,plan`: `expire = date + period_days(plan)`; schedule
`welcome@date`, `expiring@(expire-7)`, `expiring@(expire-1)`, `expired@expire`. A user can
subscribe more than once (independent schedules; see Part 3 for what "more than once" means once
cancel/renew exist).

### Part 2 — plan changes with proration
`change` becomes active. **The one rule every state-changing event obeys, always:** at event date
`d`, first **discard every email already scheduled for that user with a date strictly after `d`**
(not yet due — only those get revoked; anything dated `<= d`, including something dated exactly
`d` from an earlier event, is treated as already committed and is *never* revoked), then append
the freshly computed schedule for the new state. This single rule is what "reschedules the pending
`expiring`/`expired` emails" after a change (and, in Part 3, after a renew or cancel).

For `date,user,change,new_plan` on a user whose current period is `[.., expire)`:
* Ignored if the user is unknown, canceled, or `date >= expire` (already at/after their own expiry
  — changing an expired subscription is a no-op).
* `remaining_old = expire − date` (days). `remaining_new = remaining_old * period_days(new_plan)
  // period_days(old_plan)` — **integer floor division, always**, no rounding. `new_expire = date +
  remaining_new`.
* Apply the discard-then-reschedule rule above with `new_expire`. A `change` never itself emits an
  email — it only silently reshapes the future schedule (this is the detail that most
  differentiates cd01 from `q07`, which prints an explicit `[Changed]` line).

### Part 3 — renewals and cancellation
`renew` and `cancel` become active, on top of Part 2.

* `date,user,renew`: ignored if the user is unknown or canceled. Otherwise:
  * If `date < expire` (renewing before the term is up): `new_expire = expire +
    period_days(current_plan)` — **extended from the old expiry**, not from the renewal date.
    Emit `renewed` at `date`.
  * If `date >= expire` (renewing on/after the user's own expiry day): treated as a **brand new
    subscription** on the same plan starting `date` (`new_expire = date + period_days(plan)`).
    Emit `welcome` at `date`, not `renewed`.
  * Either way, apply the discard-then-reschedule rule with `new_expire`.
* `date,user,cancel`: ignored if the user is unknown or already canceled (idempotent — a second
  cancel is a silent no-op). Otherwise: apply the discard rule (this alone wipes every pending
  `expiring`/`expired`), emit `canceled` at `date`, and mark the user canceled. A canceled user's
  future `change`/`renew` events are ignored; a fresh `subscribe` for that user starts over
  unconditionally (it does not check the canceled flag) and is *not* itself blocked by
  cancellation.
* A `subscribe` for a user who is currently active (not canceled, not expired) is a **resubscribe**:
  the discard-then-reschedule rule applies exactly as for any other event — it wipes pending future
  emails from the old schedule and starts a fresh one.

## Worked examples
All verified by running `solution.py`.

### Example 1 (Part 1)
```
PART 1
2026-01-01,alice,subscribe,monthly
2026-01-10,bob,subscribe,annual
2026-01-01..2026-12-31
```
```
2026-01-01 alice welcome
2026-01-10 bob welcome
2026-01-24 alice expiring
2026-01-30 alice expiring
2026-01-31 alice expired
```
(alice: `expire = 2026-01-31`. bob: `expire = 2027-01-10` — annual, non-leap 2026 — so bob's
`expiring`/`expired` all fall in 2027 and are cut off by the query window; only his `welcome`
survives.)

### Example 2 (Part 2 — proration)
```
PART 2
2026-01-01,alice,subscribe,monthly
2026-01-11,alice,change,annual
2026-01-01..2026-12-31
```
```
2026-01-01 alice welcome
2026-09-04 alice expiring
2026-09-10 alice expiring
2026-09-11 alice expired
```
(`expire = 2026-01-31`; `change` on `2026-01-11` → `remaining_old = 20` days;
`remaining_new = 20 * 365 // 30 = 243`; `new_expire = 2026-01-11 + 243d = 2026-09-11`. The
originally-scheduled `expiring`/`expired` for the monthly period were all dated after `2026-01-11`
so all three are discarded and replaced.)

### Example 3 (Part 3 — renew before expiry, renew after expiry, cancel)
```
PART 3
2026-02-01,bob,subscribe,monthly
2026-02-20,bob,renew
2026-01-01,carol,subscribe,monthly
2026-02-15,carol,renew
2026-01-01,dave,subscribe,monthly
2026-01-15,dave,cancel
2026-01-01..2026-12-31
```
```
2026-01-01 carol welcome
2026-01-01 dave welcome
2026-01-15 dave canceled
2026-01-24 carol expiring
2026-01-30 carol expiring
2026-01-31 carol expired
2026-02-01 bob welcome
2026-02-15 carol welcome
2026-02-20 bob renewed
2026-03-10 carol expiring
2026-03-16 carol expiring
2026-03-17 carol expired
2026-03-26 bob expiring
2026-04-01 bob expiring
2026-04-02 bob expired
```
(bob renews on `2026-02-20`, still before his `2026-03-03` expiry → `renewed`, term extended from
the old end to `2026-04-02`. carol's monthly subscription expired `2026-01-31`; she "renews" on
`2026-02-15`, *after* expiry, so it is a fresh subscription — a `welcome`, not `renewed` — running
to `2026-03-17`; her original `welcome`/`expiring`/`expiring`/`expired` from January are untouched
because they are all dated before the renew event. dave cancels on `2026-01-15`, before any of his
`expiring`/`expired` were due, wiping all three; only `welcome` + `canceled` remain.)

## Edge cases hidden tests are known to target
- **A change/renew/cancel that lands on the exact same day as an already-scheduled `expiring` for
  the old plan does *not* revoke it** — only strictly-future dates are discarded. Concretely:
  `subscribe` annual on `2026-01-01` (`expire = 2027-01-01`, `expiring@2026-12-25`,
  `expiring@2026-12-31`), then `change,monthly` on `2026-12-31` (one day of the old period left) →
  `remaining_new = 1*30//365 = 0` → `new_expire = 2026-12-31` (immediate same-day expiry) — but
  both old `expiring` emails (`2026-12-25`, `2026-12-31`) survive because neither is *strictly
  after* the event date; the output has **two** entries dated `2026-12-31` (`expiring` then
  `expired`, per TYPE_ORDER) plus the untouched `2026-12-25 expiring`.
- `change` exactly on the user's own `expire` day is a no-op (ignored, not an error).
- `change`/`renew` for an unknown user, or for a canceled user, are silently ignored.
- a second `cancel` for an already-canceled user is a no-op (idempotent).
- resubscribing while already active wipes the old pending schedule (Part 3).
- two identical `subscribe` lines for the same user on the same day are **not deduplicated** — both
  `welcome` emails print (the second event's `<=d` cutoff keeps the first's same-day welcome);
  this is deliberate — see "面试官会怎么追问" #2.
- `remaining_old == period_days(old_plan)` (a `change` on the subscribe day itself) reduces exactly
  to a fresh subscription on the new plan, with no floor-division loss.
- events given out of chronological order in the input file must still be applied in date order.
- query window boundaries: an email dated exactly `FROM` or exactly `TO` is included; one day
  outside either bound is excluded.
- 10^5 event lines across many users, single query window — must stay near-linear.

## Variants seen in the wild
- **Day-offset / `[Changed]`+`[Renewed]` variant**: see `problems/q07_subscription_notifications` —
  same three-part shape (basics → changes → renewals), but integer day offsets instead of calendar
  dates, and explicit `[Changed]`/`[Renewed]` announcement lines instead of cd01's silent
  reschedule. Treat the two as siblings, not duplicates.
- linkjob's "2026 Java NG VO — Email Subscription" mentions a "flexible `send_schedule` structure
  handling multiple trigger types" — a generalization where the `(-7, -1, 0)` offsets and the
  `{welcome, expiring, expired}` message set become configurable, analogous to q07's
  `schedule=` parameter.
- Simplify's one-line gloss, "notification scheduling system with subscription lifecycle
  management," is consistent with, but does not add detail beyond, the above.

## What this tests
skills: S01 reading a multi-part spec · S02 line parsing with an optional trailing field · S03
per-user mutable state · S08 deterministic multi-key sort with a fixed (not input-derived)
tie-break · S09 exact formatting · S10 event streams that retroactively change earlier decisions ·
S12 calendar-date arithmetic (`timedelta`, non-leap-year annual periods) · S19 incremental design
(subscribe-only → +change/proration → +renew/cancel)

## Sources
- `loop/raw/en_forums.md` §6.2 C1 (line ~303-306): "Part 1: 按 plan 日期发邮件（welcome、expiration
  notices）。Part 2: 根据用户输入处理 plan 变更。Part 3: 续费/延期。" [linkjob intern, 2025]; "2026
  Java NG VO - Email Subscription" flexible `send_schedule` [linkjob technical, 2025-12-08];
  Simplify one-line gloss [Simplify, 2026].
- `loop/raw/cn_forums.md` line 99: 一亩三分地「Subscription Email Scheduler」导读，TOC = Part 1
  Scheduling Basics → Part 2 Changing Plans → Part 3 Handling Renewals → Solution Strategy →
  Common Follow-up Questions. [1point3acres.com/interview/post/7100084]
- `loop/raw/cn_forums.md` line 264: 一亩三分地「Email Notification Scheduler」(`oj` 类型, 正文完整):
  "常见追问：同一用户+类型在时间窗口内的去重/合并、按用户限流、同 `sendAt` 多任务的排序、乱序到达、
  取消/更新逻辑". These five follow-up directions are folded into "面试官会怎么追问" below.
- `problems/q07_subscription_notifications/problem.md` — the sibling day-offset variant this
  problem deliberately does not duplicate.

## 面试官会怎么追问
1. 如果同一批事件里，同一个 user 同一天出现多条几乎相同的事件（比如客户端重试导致同一个
   `subscribe` 或 `change` 被发送了两次），你现在的实现会不会重复发邮件？上面的"重复 subscribe"边
   界例就是这个问题的答案（会重复）——你会怎么改成幂等的？给事件一个唯一 id 去重，还是在应用状态变
   更前先比较"新状态是否和当前状态相同"？
2. 如果要求"同一个用户同一天最多收 1 封邮件"（合并/限流），你会怎么在现在的排序结果上做后处理？
   直接在最终列表里按 `(date,user)` 分组只保留第一条，还是需要更细的合并规则（比如 `expired` 优
   先于 `expiring`）？
3. 输入目前假设一次性给全量事件、离线批处理；如果改成**流式**处理（事件一条条实时到达，不能重新
   排序整批数据），你的"先丢弃未来邮件再重新排程"这套模型还能用吗？需要什么样的数据结构（比如每
   个用户维护一个按日期排序的小根堆/有序容器）来保证仍然是"当前决定不了未来"的语义？
4. 现在的日期都是"请求处理所在时区"的日历日期；如果客户端传的是 UTC 时间戳，而"到期前 7 天"要按
   用户本地时区（比如美国有夏令时）计算，你的 `timedelta(days=7)` 还成立吗？DST 切换的那一周会怎
   么错位？
5. 10^5 到 10^6 条事件规模下，你的每用户"丢弃未来邮件再重建"操作复杂度是多少？是否会退化（比如一
   个用户反复 change 上千次，每次都线性扫描该用户的 pending 列表）？怎么用堆/平衡树把单用户操作降
   到 `O(log k)`（`k` = 该用户 pending 邮件数，通常 ≤ 3，所以其实已经是常数级——但如果 schedule 表
   项变多，比如从 3 种邮件类型变成 20 种，这个假设还成立吗）？
6. 如果乱序输入不只是"文件里行序打乱"，而是**真的乱序到达**（网络延迟导致一个更早日期的事件在一个
   更晚日期的事件处理完之后才到达），"先处理完的决定不可撤销"这个假设会被打破——你会怎么设计一个
   "宽限期"（grace period）让系统能接受一定程度的迟到事件而不必假装它们没发生？
7. 如果要支持"取消"之外的第四种终止状态，比如"暂停"（pause，之后可以 resume 且到期日顺延暂停天
   数），你的状态机（`plan`, `expire`, `canceled`）要怎么扩展？`resume` 事件的到期日顺延逻辑和
   `change` 的比例重算逻辑有什么本质区别？
