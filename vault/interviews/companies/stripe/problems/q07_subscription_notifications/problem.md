# q07 · Subscription Notification Scheduler — welcome / expiry-warning / expired emails, plan changes, renewals

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min, 3 parts; also seen as an intern VO / onsite prompt) · **Last asked:** 2026-02-10 (extrabrain problem set)
**Frequency:** 6 independent mentions (extrabrain 2026-02-10, linkjob 2025-09-16, oavoservice 2025-12-27, 1point3acres 题库 「Email Subscription」, 1point3acres 1100699 intern VO, prachub 「Generate Account Email Notifications」) · **Confidence:** medium-high

## Context
Stripe Billing sends lifecycle emails for every subscription: a welcome mail when it starts, a
warning shortly before it ends, and a notice when it has expired. Customers also change plans
and renew mid-term, which changes what later emails must say and when they go out. You are
given the subscription records plus a stream of lifecycle events and must print the exact
sequence of emails the system will send, in the order it will send them.

**Time model:** all dates are integer **day offsets** (day 0, day 1, …) — there are no calendar
dates, months or leap years in this problem. A subscription that starts on day `s` with
duration `d` is active on days `s .. s+d-1`; its **end day is `s + d`**, the first day on
which it is no longer active (i.e. the end day is *exclusive* of the active period, and the
"expired" email is sent on that day).

## Input (stdin)
First line `PART n` (`n ∈ {1,2,3,4}`). Then one record per line; blank lines are ignored and
spaces around commas are tolerated.

* **User record** (Parts 1–3): `name,plan,start_day,duration_days` — `name` is unique
  (a repeated name replaces the earlier record and takes the later position), `plan` is a
  free string without commas, `start_day ≥ 0`, `duration_days ≥ 0`.
* **Plan-change event** (Part 2+): `CHANGE,name,new_plan,day`
* **Renewal event** (Part 3+): `RENEW,name,extra_days,day`
* **Part 4 (rule-driven variant)**: first line after `PART 4` is `current_day`; then
  `ACCOUNT,account_id,created_day,expires_day` and
  `RULE,rule_name,trigger,offset_days,template` lines (`template` is the remainder of the line
  and may contain spaces and commas; `trigger ∈ {on_create, days_before_expiration, after_expiration}`).

The first field `CHANGE` / `RENEW` / `ACCOUNT` / `RULE` is reserved and identifies the line
type; anything else is a user record. Events naming an unknown user are ignored. Parts 1–3
ignore event types they do not support (Part 1 ignores all events, Part 2 ignores `RENEW`).
Up to 10^5 users + 10^5 events.

## Output
Parts 1–3: one line per email/event, `day: name - message` for emails and
`day: [Changed] name - old_plan -> new_plan` / `day: [Renewed] name - old_end -> new_end` for
events. **Chronological by day; ties broken by (a) user input order, (b) events before emails,
(c) events in input order / emails in schedule order (welcome, warning, expired).**
Part 4: `account_id rule_name template` lines, accounts in input order then rules in
configuration order. Nothing is printed for an empty input.

## Rules
### Part 1 — send schedule
The send schedule is a list of `(when, message)` pairs, default:

| when    | day sent             | message              |
|---------|----------------------|----------------------|
| `start` | `start_day`          | `Welcome to <plan>`  |
| `-15`   | `end_day - 15`       | `Upcoming expiry`    |
| `end`   | `end_day`            | `Subscription expired` |

with `end_day = start_day + duration_days`. A negative offset counts back from the end day.
**An email whose day is earlier than `start_day` is not sent** (a 10-day subscription gets no
warning; a 15-day one gets the warning on its start day, printed after the welcome).

### Part 2 — plan changes
`CHANGE,name,new_plan,day` takes effect **at the start of `day`** (before that day's emails):
print `day: [Changed] name - old -> new` and every email dated `≥ day` uses the new plan name
(the welcome, if the change precedes the start day). Dates are unchanged; a plan change never
produces an "expired" email for the old plan. A change to the same plan is still printed.

### Part 3 — renewals
`RENEW,name,extra_days,day` takes effect at the start of `day`: print
`day: [Renewed] name - old_end -> new_end` with `new_end = old_end + extra_days` (the term is
extended from the old end, whatever the renewal day). Then the user's schedule is
**recomputed from the new end**, under this exact rule:

> An email is sent iff its day is `≥ start_day` **and** `≥` the day of the last event that
> recomputed the schedule. Emails dated before the event are already sent and are **never
> un-sent**; pending ones (dated `≥ day`) are replaced by the recomputed ones.

Consequences: a warning already sent before the renewal stays and a second warning is sent
15 days before the new end (if that is `≥ day`); renewing on the end day itself suppresses the
"expired" email (`new_end > day`); renewing after expiry keeps the old "expired" email and
sends a second one on the new end only if `new_end ≥ day`. Events are processed in day order,
ties by input order; `CHANGE` and `RENEW` may mix.

### Part 4 — rule-driven variant (prachub "Generate Account Email Notifications")
`schedule_by_rules(current_day, accounts, rules)`: for the single day `current_day`, a rule
fires for an account when
`on_create`: `current_day == created_day + offset_days`;
`days_before_expiration`: `current_day == expires_day - offset_days`;
`after_expiration`: `current_day == expires_day + offset_days`.
Output `"<account_id> <rule_name> <template>"`, accounts in input order, rules in
configuration order. Must be near-linear (≤ 2·10^5 lines).

## Worked examples
### Example 1 (Part 1)
```
PART 1
Alice,basic,0,30
Bob,pro,10,30
```
```
0: Alice - Welcome to basic
10: Bob - Welcome to pro
15: Alice - Upcoming expiry
25: Bob - Upcoming expiry
30: Alice - Subscription expired
40: Bob - Subscription expired
```
(Alice: end 30 → warning 15; Bob: end 40 → warning 25.)

### Example 2 (Part 2)
```
PART 2
Alice,basic,0,30
Bob,pro,10,30
CHANGE,Alice,premium,5
CHANGE,Bob,enterprise,10
```
```
0: Alice - Welcome to basic
5: [Changed] Alice - basic -> premium
10: [Changed] Bob - pro -> enterprise
10: Bob - Welcome to enterprise
15: Alice - Upcoming expiry
25: Bob - Upcoming expiry
30: Alice - Subscription expired
40: Bob - Subscription expired
```
(Bob's change lands on his start day → it is applied first, so the welcome names `enterprise`.)

### Example 3 (Part 3)
```
PART 3
Alice,basic,0,30
RENEW,Alice,30,20
```
```
0: Alice - Welcome to basic
15: Alice - Upcoming expiry
20: [Renewed] Alice - 30 -> 60
45: Alice - Upcoming expiry
60: Alice - Subscription expired
```
(The day-15 warning was already sent; the pending day-30 expiry is replaced by day 60 and a
new warning at 45.)

### Example 4 (Part 3, renewal on the end day and after expiry)
```
PART 3
Alice,basic,0,30
Bob,pro,0,30
RENEW,Alice,10,30
RENEW,Bob,10,31
```
```
0: Alice - Welcome to basic
0: Bob - Welcome to pro
15: Alice - Upcoming expiry
15: Bob - Upcoming expiry
30: [Renewed] Alice - 30 -> 40
30: Bob - Subscription expired
31: [Renewed] Bob - 30 -> 40
40: Alice - Subscription expired
40: Bob - Subscription expired
```
(Alice renews on day 30 → no expiry on 30; new warning day 25 < 30 → not sent. Bob renews on
31, after the expiry email already went out → it stays; second expiry on 40.)

### Example 5 (Part 4)
```
PART 4
30
ACCOUNT,acc_1,0,30
ACCOUNT,acc_2,30,60
ACCOUNT,acc_3,0,45
RULE,welcome,on_create,0,Welcome aboard
RULE,warn,days_before_expiration,15,Your plan expires in 15 days
RULE,bye,after_expiration,0,Your plan has expired
```
```
acc_1 bye Your plan has expired
acc_2 welcome Welcome aboard
acc_3 warn Your plan expires in 15 days
```

## Edge cases hidden tests are known to target
- warning day before the start day (duration < 15) → no warning; duration == 15 → warning on
  the start day, after the welcome; duration 0 → welcome and expired on the same day
- same-day ties: user input order, then event before email, then schedule order
- `CHANGE` on the start day → welcome uses the new plan; `CHANGE` after the start → only the
  `[Changed]` line is visible
- renewal before / on / after the warning day, on the end day, after expiry (examples 3–4)
- two events for one user on the same day (input order), events given out of day order
- events for unknown users are ignored; extra_days = 0 still prints `[Renewed] 30 -> 30`
- exact format: `day: name - message`, `[Changed]`/`[Renewed]` tags with a space, `->` with
  spaces, no trailing spaces
- Part 4: accounts created and expiring on the same day, rule that matches nothing, offsets 0

## Variants seen in the wild
- **Rule-driven single-day variant** (prachub): implemented as Part 4 / `schedule_by_rules`.
- Calendar dates (`YYYY-MM-DD`) instead of day offsets, with a `datetime.timedelta` for the −15
  days (1point3acres 题库 「Email Subscription」 VO form). Same logic; parse with
  `date.fromisoformat` and format back with `isoformat()`.
- Tie-break "by subscription id" (linkjob) — here the id is the user's input position.
- A fourth part in some VO rounds: cancellation event → no further emails (not implemented;
  it is a `RENEW`-like event that sets `end = day` and drops pending emails).
- Custom `send_schedule` mappings (other offsets such as `-7`, `-1`) — pass `schedule=` to
  `part1/part2/part3`.

## What this tests
skills: S01 reading a long spec · S02 line parsing with mixed record types · S03 records keyed
by id · S08 deterministic multi-key sort · S09 exact formatting with tags · S10 event streams
that change earlier decisions · S12 day-offset arithmetic · S19 incremental design (parse →
state → schedule → render)

## Sources
- https://extrabrain.app/interview-questions/stripe-hackerrank-online-assessment-extrabrain/ (2026-02-10; OA, 3 parts)
- https://www.linkjob.ai/interview-questions/stripe-hackerrank-online-assessment/ (2025-09-16; OA, 3 parts)
- https://www.linkjob.ai/interview-questions/stripe-interview-questions/ (2025-12-07; intern VO mention)
- oavoservice.com 2025-12-27 (Chinese write-up; same 3-part structure)
- 1point3acres 题库 `problems/4d6938ea-…` 「Email Subscription」; 1point3acres 1100699 「2025 intern team screen+VO」 (VO: Email Subscription)
- prachub 「Generate Account Email Notifications」 (rule-driven variant, full spec; ≤ 2·10^5 lines)
- collegesidekick repost of 1point3acres 793600 (onsite: "email notification for invoice events")
