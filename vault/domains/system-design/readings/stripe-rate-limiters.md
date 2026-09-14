---
nodes: [traffic.rate-limiting]
url: https://stripe.com/blog/rate-limiters
tags: [canonical, stripe]
---
# Scaling your API with Rate Limiters (Stripe)

The industry-standard post on rate limiting in production — not just the
algorithms, but the four distinct limiter types Stripe runs and how they shed
load without hurting real users.

**Extract on read:**
- Token bucket as the workhorse; where sliding windows earn their extra cost.
- Request-rate limiters vs concurrency limiters vs fleet-usage load shedders — different problems.
- Return 429 with Retry-After, and dark-launch limiters in log-only mode first.

%% trellis:begin %%
## Source
[Open the original ↗](https://stripe.com/blog/rate-limiters)

## Archived copy
![[stripe-rate-limiters-clip]]
%% trellis:end %%
