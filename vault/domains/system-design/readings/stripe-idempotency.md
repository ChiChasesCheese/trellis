---
nodes: [correctness.idempotency]
url: https://stripe.com/blog/idempotency
tags: [canonical, fintech, stripe]
---
# Designing robust and predictable APIs with idempotency (Stripe)

The industry-standard treatment of idempotency keys for money movement —
short, and every payments interviewer has read it.

**Extract on read:**
- Client-generated keys + server-side dedup window.
- Replaying the *stored response* vs re-executing the operation.
- How retries, timeouts, and idempotency compose into an end-to-end guarantee.

Related cards: [[correctness-idempotency-key-design]], [[correctness-dedup-window]], [[correctness-idempotency-concurrent-retries]]

%% trellis:begin %%
## Source
[Open the original ↗](https://stripe.com/blog/idempotency)

## Archived copy
![[stripe-idempotency-clip]]
%% trellis:end %%
