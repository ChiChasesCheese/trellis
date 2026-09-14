---
nodes: [model.idempotency]
url: https://docs.stripe.com/api/idempotent_requests
tags: [docs]
---
# Idempotent requests (Stripe API reference)

The shortest precise statement of what idempotency actually promises, from a
system that has to get it right at scale. A client sends a key; the server
performs the operation at most once and replays the stored response for any
repeat. The details are the interesting part: keys expire, a repeat with a
*different* payload is an error rather than a silent overwrite, and a request
still in flight gets a concurrency error rather than a second execution.

**Extract on read:**
- "At most once, replay the recorded result" — a repeat is a no-op that still
  returns the original answer, not nothing.
- Same key with different parameters is an error; that is the rule an assessment
  usually states as "a duplicate id with a different amount is rejected".
- Key expiry, and why idempotency is a property of a window rather than forever.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.stripe.com/api/idempotent_requests)

## Archived copy
![[stripe-idempotent-requests-clip]]
%% trellis:end %%
