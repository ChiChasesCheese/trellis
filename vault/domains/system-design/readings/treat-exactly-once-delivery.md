---
nodes: [async.delivery.guarantees]
url: https://bravenewgeek.com/you-cannot-have-exactly-once-delivery/
tags: [canonical]
---
# You Cannot Have Exactly-Once Delivery (Tyler Treat)

Walks the delivery-guarantee ladder from first principles: why at-most-once and
at-least-once are the only two *delivery* semantics a network can offer, and why
the Two Generals problem makes the third one a marketing claim. Ends where every
real design ends — idempotent consumers and deduplication.

**Extract on read:**
- Ack-before-process gives at-most-once; ack-after-process gives at-least-once. There is no third choice.
- Exactly-once *delivery* is impossible; exactly-once *processing* is achievable by making handlers idempotent.
- The knock-on costs of at-least-once: dedup state, ordering only within a partition, dead-letter queues for poison messages.

%% trellis:begin %%
## Source
[Open the original ↗](https://bravenewgeek.com/you-cannot-have-exactly-once-delivery/)

## Archived copy
![[treat-exactly-once-delivery-clip]]
%% trellis:end %%
