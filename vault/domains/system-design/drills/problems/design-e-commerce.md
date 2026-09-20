---
nodes: [problems.commerce.e-commerce, correctness.saga, correctness.outbox]
tags: [problem]
---
# Drill: Design the core purchase flow for an e-commerce platform (Amazon-style)

Users browse product pages, add items to a cart (anonymous or logged in), and check out.
Third-party sellers list their own prices and stock against a shared product catalogue.
Assume 50M DAU, ~1.2B product-page views/day, and ~850,000 orders/day.

**Constraints to state and honor**
- Product-page read latency target P99 < 150ms, served overwhelmingly from cache/CDN.
- Inventory must never oversell at the moment of checkout; the catalogue's displayed
  stock is allowed to be a few seconds stale.
- An order, once created, must never be silently lost, even if payment, fulfillment or
  notification is temporarily unavailable.
- The same order can contain items from multiple sellers, each with independent price,
  stock, and refund/settlement.

**Grading points**
- Assigns a different consistency guarantee to catalogue, cart, checkout/inventory, and
  order instead of one model for everything, and can say why each domain needs its own
  ([[problems-e-commerce-five-consistency-domains]]).
- Computes the product-page read:write ratio and derives that it must be served from
  cache/CDN with layered freshness rather than the source of truth
  ([[problems-e-commerce-read-write-ratio-drives-caching]]).
- Computes ordinary-SKU inventory-decrement QPS and argues it fits under a relational
  primary's conditional-update ceiling — only a promoted/contended SKU needs the
  flash-sale-style atomic-decrement path ([[problems-e-commerce-inventory-decrement-below-relational-ceiling]]).
- Designs the cart split — anonymous in a TTL-bound store, logged-in durable, merged once
  explicitly at login — and explains why continuous sync isn't needed
  ([[problems-e-commerce-cart-anonymous-vs-logged-in]]).
- Reserves inventory at checkout-start with a short TTL rather than at add-to-cart or only
  after payment succeeds, and can state the oversell/undersell trade each alternative makes
  ([[problems-e-commerce-reservation-timing-tradeoff]]).
- Orders the order saga's steps so the hardest-to-compensate action (fulfillment) comes
  last, after payment, after inventory reservation
  ([[problems-e-commerce-order-saga-pivot-ordering]], [[correctness-saga-compensation-limits]]).
- Writes the order and the saga-kickoff event in one local transaction (transactional
  outbox) instead of writing then publishing separately
  ([[problems-e-commerce-outbox-for-checkout]], [[correctness-outbox-mechanism]]).
- For the marketplace variant, precomputes the buy box for read performance but refreshes
  it on a seller-side price/stock change event, not only on a batch schedule
  ([[problems-e-commerce-marketplace-buy-box-refresh]]).
- Can reason about a Black Friday traffic spike from the computed numbers: the order-write
  path stays within normal capacity while the read path needs cache pre-warming and
  admission control for specifically promoted SKUs
  ([[problems-e-commerce-black-friday-order-vs-read-scaling]]).
- Recognizes when a scenario has degenerated into the flash-sale problem (a single SKU
  under extreme contention) and reaches for that design instead of reinventing it
  ([[problems-e-commerce-black-friday-order-vs-read-scaling]]).

**Solution**: [[solution-e-commerce]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
