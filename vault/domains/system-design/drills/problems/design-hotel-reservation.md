---
nodes: [problems.commerce.hotel-reservation, distributed.transactions.isolation]
tags: [problem]
---
# Drill: Design a hotel/marketplace reservation system like Airbnb

Design the search and booking paths for a platform with 6 million active listings
(about 9 million bookable room-types), a 365-day booking window, 1,000,000 bookings/day
and 50,000,000 search sessions/day. Some properties also sell the same physical rooms
through an external OTA channel.

**Constraints to state and honor**
- A booking locks a contiguous range of nights (average 3) on one room-type; the whole
  range must succeed or fail together, never partially.
- Search and booking are separate paths with a read:write ratio of about 50:1 — search
  must never share load with the booking path's database.
- Room-type inventory may be deliberately overbooked, up to a risk budget the property
  configures (e.g. ≤1% chance of exceeding physical capacity), not sold with zero slack.
- A property syncing with an external channel must reconcile conflicting confirmations
  within a bounded delay (target P99 < 2 minutes), since the two systems don't share a
  database transaction.

**Grading points**
- Models inventory as one row per room-type per night with a total/booked counter (not
  one row per physical unit), and explains why pooling beats early physical-unit binding
  for interchangeable rooms ([[problems-hotel-reservation-per-night-inventory-model]]).
- Makes a multi-night booking one multi-row conditional UPDATE guarded by the WHERE
  clause, and explicitly checks the affected-row count against the number of nights
  before committing, rolling back on a partial match ([[problems-hotel-reservation-multirow-conditional-update-rollback]]).
- Explains why a naive "SELECT remaining, then UPDATE" pattern double-books under
  read-committed isolation (write skew), and why folding the check into the UPDATE's
  WHERE clause fixes it without raising the isolation level ([[problems-hotel-reservation-check-then-write-double-books]], [[distributed-isolation-anomalies]], [[distributed-write-skew]]).
- Derives the read:write QPS gap from DAU/search-conversion assumptions and explains why
  this system's booking peak-to-average ratio is far gentler than a single-event ticket
  sale's, and doesn't need a virtual queue ([[problems-hotel-reservation-peak-booking-vs-search-qps]]).
- Separates the search path (denormalized, minutes-stale index for candidate generation)
  from an authoritative per-room availability query, and justifies why pricing every
  candidate on every search doesn't scale ([[problems-hotel-reservation-search-index-vs-booking-path]]).
- Sizes an overbooking policy from a no-show rate and a risk budget rather than applying
  one flat percentage everywhere, and can explain why the safe percentage grows with
  pool size ([[problems-hotel-reservation-overbooking-risk-budget]]).
- Treats an external channel's booking confirmation as another writer racing for the same
  conditional update, and designs a reconciliation path for whichever side loses the race
  ([[problems-hotel-reservation-cross-channel-conflict]]).
- Calls out at least one failure mode (inventory DB primary down, search index stale) and
  states whether each path should degrade availability or degrade consistency.

**Solution**: [[solution-hotel-reservation]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
