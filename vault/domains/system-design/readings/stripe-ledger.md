---
nodes: [correctness.ledger]
url: https://stripe.com/blog/ledger-stripe-system-for-tracking-and-validating-money-movement
tags: [stripe, fintech]
---
# Ledger: Stripe's system for tracking and validating money movement

Stripe's internal double-entry ledger described as a real production system,
not a textbook exercise: immutable events, derived balances, and — the part
most write-ups skip — treating discrepancy detection and clearing as a
first-class, continuously measured process. Directly answers "how do you know
the money numbers are right?" at interview depth.

**Extract on read:**
- Modeling money movement as immutable events; balances derived, never stored as mutable truth.
- Mapping heterogeneous upstream systems onto one common ledger abstraction.
- Discrepancy detection as a metric: what "clearing" a discrepancy means and how teams are held to it.
- The trust-but-verify loop between the ledger and the source systems it mirrors.

%% trellis:begin %%
## Source
[Open the original ↗](https://stripe.com/blog/ledger-stripe-system-for-tracking-and-validating-money-movement)

## Archived copy
![[stripe-ledger-clip]]
%% trellis:end %%
