---
nodes: [problems.commerce.ticket-booking, distributed.transactions.isolation]
tags: [problem]
---
# Drill: Design a ticket booking platform like Ticketmaster

Design the booking path for a 50,000-seat stadium show: assigned seating, seat holds
while the buyer pays, and no double-selling when a million buyers hit the on-sale in the
first minute.

**Constraints to state and honor**
- 50,000 seats, roughly 1,000,000 buyers competing in the first minute of the on-sale.
- A held seat must auto-release if the buyer doesn't complete payment within 10 minutes.
- Never oversell a seat, even under database or cache failure — correctness beats availability on the write path.
- Read (seat-map) traffic can run ~700x write (hold) traffic at peak; the read path must never hit the seat database directly.

**Grading points**
- Models seats as one row per seat with a status machine (available/held/sold), not a shared decrement counter, and explains why the counter model fails for assigned seating ([[problems-ticket-booking-hold-vs-decrement-model]]).
- Makes the available→held transition a single atomic conditional UPDATE rather than a cross-request lock or a cron-based expiry sweep ([[problems-ticket-booking-seat-state-conditional-update]]).
- Argues correctly why read-committed isolation suffices for that single-statement update, and where the design would need serializable isolation or explicit locks instead ([[problems-ticket-booking-isolation-write-skew-risk]], [[distributed-write-skew]]).
- Explains why per-row contention (~20:1 average) is not the real database bottleneck, and derives the actual aggregate write-QPS gap that forces a virtual queue ([[problems-ticket-booking-hold-vs-lock-contention]]).
- Designs a virtual waiting room whose admission rate is throttled to what the seat database can sustain, ideally with a feedback signal ([[problems-ticket-booking-virtual-queue-admission]]).
- Addresses the hottest seats (e.g. 2,500:1 contention in a VIP section) with a mitigation that doesn't touch the core data model, such as candidate-set booking ([[problems-ticket-booking-hot-seats-candidate-set]]).
- Extends the hold during checkout and structures payment as a reserve→charge→confirm saga, idempotent on the hold id, so a duplicate webhook can't double-charge or double-sell ([[problems-ticket-booking-payment-hold-extension-saga]]).
- Calls out at least one failure mode (Redis down, seat DB primary down, PSP timeout) and states whether the system should fail open or fail closed for it.

**Solution**: [[solution-ticket-booking]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
