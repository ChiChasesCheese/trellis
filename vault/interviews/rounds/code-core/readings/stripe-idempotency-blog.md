---
nodes: [model.idempotency, transfer.stripe-oa]
url: https://stripe.com/blog/idempotency
tags: [canonical]
---
# Designing robust and predictable APIs with idempotency (Stripe)

The long-form version of why repeated events exist at all: networks fail
ambiguously, so a client that does not retry loses work and a client that does
retry duplicates it. The essay walks through idempotency keys, the state machine
a partially-completed operation needs, and why foreign state mutations have to be
made recoverable. It is also the clearest available description of the mental
model behind the event-with-reversals problems these assessments are built from.

**Extract on read:**
- Why a retry is guaranteed, not hypothetical — and therefore why de-duplication
  is a requirement rather than a nicety.
- Recording the *result* alongside the key, so a replay returns the original
  answer ([[cc-transfer-oa-payments-vocabulary]]).
- Breaking a multi-step operation into recoverable stages — the same reasoning
  that makes an event stream replayable.

%% trellis:begin %%
## Source
[Open the original ↗](https://stripe.com/blog/idempotency)

## Archived copy
![[stripe-idempotency-blog-clip]]
%% trellis:end %%
