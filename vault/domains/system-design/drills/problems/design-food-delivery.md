---
nodes: [problems.geo.food-delivery, correctness.saga]
tags: [problem]
---
# Drill: Design a food and grocery delivery platform like DoorDash/Gopuff

Design the backend for a delivery platform that has to support two variants: a three-sided
marketplace connecting consumers, independent restaurants, and couriers (DoorDash), and a
single-party local-inventory service where the platform owns micro-fulfillment centers and
their stock (Gopuff). Cover catalog/inventory, checkout orchestration, courier dispatch, and
live tracking.

**Constraints to state and honor**
- Roughly 114 orders/second nationally on average, peaking around 477 orders/second in the
  busiest dinner minute; a single dense market's peak is a fraction of that.
- Availability/menu-browsing read traffic runs about 20x the order write traffic.
- Zero tolerance for overselling a specific Gopuff inventory row; DoorDash's merchant
  acceptance step is the real backstop against a stale "available" flag, not a hard
  guarantee at browse time.
- Dispatch has a looser SLA than ride-hailing (minutes, not seconds), which is what makes
  batching orders across a short window viable.

**Grading points**
- Explains why availability/menu reads and the inventory-decrement write need very different
  consistency and caching treatment given their traffic ratio
  ([[problems-food-delivery-read-write-ratio-cache-vs-strong-consistency]]).
- Distinguishes DoorDash's coarse merchant-set availability flag (backstopped by order
  acceptance) from Gopuff's precise, strongly-consistent conditional inventory decrement, and
  explains why neither mechanism can substitute for the other
  ([[problems-food-delivery-two-consistency-granularities]]).
- Designs checkout as an explicit saga and can explain why the compensating action for a
  failure depends on whether payment has already been captured, not just authorized
  ([[problems-food-delivery-saga-compensation-capture-timing]]).
- Argues why courier dispatch should be a periodic batched optimization over greedy
  nearest-match, and backs it with a concrete batch-size number that shows the optimization
  is computationally tractable, not just theoretically nicer
  ([[problems-food-delivery-batched-mip-vs-greedy-dispatch]],
  [[problems-food-delivery-batch-window-order-count]]).
- Recognizes dispatch timing (when to send a courier to the restaurant) as a distinct problem
  from matching (which courier), and describes a concrete sensor-fusion mechanism for it
  ([[problems-food-delivery-uber-eats-crf-dispatch-timing]]).
- States a concrete fix for write contention on a single hot inventory row during a
  promotion, without breaking the read side ([[problems-food-delivery-hot-sku-sharded-counters]]).
- Explains what has to change about the dispatch optimizer at 10x order volume
  ([[problems-food-delivery-10x-mip-degrades-heuristic]]).
- Connects courier location tracking and live-order tracking to the same high-frequency,
  no-transaction ingestion pattern used for driver location in ride-hailing, without
  re-deriving it ([[problems-ride-hailing-ingestion-vs-matching-order-of-magnitude]]).

**Solution**: [[solution-food-delivery]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
