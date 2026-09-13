---
nodes: [caching.model, caching.hierarchy, caching.stampede, caching.failure]
url: https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
tags: [canonical]
---
# Caching Challenges and Strategies (AWS Builders' Library)

Amazon's production account of caches as both acceleration and a new failure
mode. It connects local versus external caches, cold starts, request coalescing,
soft/hard TTLs, negative caching, and the dangerous fallback to an undersized
origin.

**Extract on read:**
- Compare local and external cache failure/cold-start behavior.
- Defend against a thundering herd with more than one mechanism.
- Test cache loss without turning fallback traffic into a downstream brownout.

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/caching-challenges-and-strategies/)
%% trellis:end %%
