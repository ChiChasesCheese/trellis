---
nodes: [reliability.resilience.retries]
url: https://sre.google/sre-book/handling-overload/
tags: [canonical]
---
# Handling Overload (Google SRE Book, ch. 21)

The one chapter that puts timeouts, deadlines and retries in the same frame:
client-side throttling, a per-request *retry budget*, and deadline
propagation down the call chain — with the arithmetic showing how a
3-attempt policy at every layer becomes a 27x amplification on a 3-deep stack.

**Extract on read:**
- Retry budget: cap retries at ~10% of requests, retry only on the layer that saw the error, and return "overloaded; don't retry" upward instead of retrying blind.
- Deadline propagation: every hop passes the *remaining* budget, and a server checks the deadline before it starts work — otherwise the fleet burns CPU on requests the caller already abandoned.
- Client-side throttling (adaptive request rejection) keeps a client from hammering a backend that is already shedding, and criticality tags decide what gets shed first.

%% trellis:begin %%
## Source
[Open the original ↗](https://sre.google/sre-book/handling-overload/)

## Archived copy
![[google-sre-handling-overload-clip]]
%% trellis:end %%
