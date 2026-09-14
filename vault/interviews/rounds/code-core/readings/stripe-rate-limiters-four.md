---
nodes: [chrono.windows, algorithms.sliding-window]
url: https://stripe.com/blog/rate-limiters
tags: [canonical]
---
# Scaling your API with rate limiters (Stripe)

A production account of four different limiters — request rate, concurrency,
fleet usage and worker utilization — and why each exists. Read it for the token
bucket implementation and for the discussion of what a limiter must do at the
boundary: whether the window is open or closed at each end, what a rejected
request costs, and why denied requests must not themselves extend the lockout.

**Extract on read:**
- Token bucket versus fixed and sliding windows, and the memory each costs per key.
- Refill computed lazily from elapsed time, in integers, so no drift accumulates
  ([[cc-python-pitfalls-float-equality]]).
- The boundary question every windowed rule has: is `t - W` included or excluded
  ([[cc-verification-edge-exact-threshold-triple]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://stripe.com/blog/rate-limiters)

## Archived copy
![[stripe-rate-limiters-four-clip]]
%% trellis:end %%
