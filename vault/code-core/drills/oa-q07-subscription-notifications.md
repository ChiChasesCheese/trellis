---
nodes: [model.event-stream, output.ordering, transfer.stripe-oa]
tags: [stripe-oa, q07]
---
# Drill: schedule and rewrite subscription lifecycle emails

Sixty minutes, stdin to stdout, no libraries beyond the standard one. Every
subscription starts on an integer day offset with a duration; it is active on
days `start .. start+duration-1` and its end day, `start+duration`, is the
first inactive day. Three lifecycle emails fire per subscription (welcome on
the start day, an "upcoming expiry" warning 15 days before the end, "expired"
on the end day itself), except an email dated before the start day is
dropped entirely. Later events change what still-pending emails must say.
Print the full chronological sequence of emails and events.

- Part 1: parse subscriptions and print their base three-email schedule.
- Part 2: add `CHANGE` events — a plan-name change effective at the start of a
  given day, which relabels every email from that day onward and prints its
  own `[Changed]` line.
- Part 3: add `RENEW` events — extend the subscription's end day and
  recompute the schedule under the rule "an email already sent stays sent; an
  email is pending, and gets recomputed, iff its day is on or after both the
  start day and the day of the event that triggered the recompute."
- Part 4: a separate, rule-driven single-day variant — given a set of
  accounts (creation/expiry day) and configurable rules (`on_create`,
  `days_before_expiration`, `after_expiration`, each with an offset and a
  template), print which rules fire for which accounts on one given day.

**Constraints to state and honor**
- Up to ~10^5 users and ~10^5 events (Parts 1-3); Part 4 must stay near-linear
  over up to 2*10^5 lines.
- A repeated user name replaces the earlier record and moves to the later
  input position for tie-breaking purposes.
- Events naming an unknown user are silently ignored; a renewal's new end is
  computed from the subscription's *old* end, not from the renewal's own day.
- Output ties break in a fixed three-level order: chronological day, then
  user input order, then events before emails on the same user/day (events in
  input order, emails in fixed welcome/warning/expired schedule order).

**Grading points**
- The "already sent vs. still pending" split is the crux of Part 3: emails
  dated strictly before the triggering event's day are locked in and never
  retroactively changed; only emails dated on or after that day (and on or
  after the subscription's start) get recomputed against the new schedule.
- A renewal on the exact end day suppresses that day's "expired" email
  (because the new end now exceeds the day); a renewal after expiry leaves
  the already-sent "expired" email alone and can produce a second one later.
- `extra_days = 0` still prints a `[Renewed] old -> old` line — a renewal
  event is never silently absorbed just because it changes nothing.
- The exact three-level tie-break is implemented as an explicit sort key, not
  approximated by insertion order alone, since events can arrive out of day
  order in the input.
- Part 4 is architecturally separate from Parts 1-3 (single day, rule table,
  no event stream) — a candidate should recognize it's a different model
  rather than trying to force-fit the earlier state machine onto it.
- Boundary durations exercised: duration < 15 (no warning at all), duration
  exactly 15 (warning lands on the start day, after the welcome), and
  duration 0 (welcome and expired the same day).

**Source**
- `vault/stripe/q07_subscription_notifications/question.md`
- `vault/stripe/q07_subscription_notifications/solution.md`
- `vault/Quick_Check/problems/q07_subscription_notifications/problem.md`
- `vault/Quick_Check/problems/q07_subscription_notifications/REPORT.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
