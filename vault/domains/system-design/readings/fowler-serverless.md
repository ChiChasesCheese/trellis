---
nodes: [architecture.serverless]
url: https://martinfowler.com/articles/serverless.html
tags: [canonical]
---
# Serverless Architectures (Mike Roberts, on martinfowler.com)

The most complete and level-headed long-form treatment of FaaS — execution
model, cold starts, state, vendor lock-in — kept updated on the most stable
architecture site on the web.

**Extract on read:**
- The FaaS execution model: stateless, event-triggered, scale-to-zero — and why state must live elsewhere.
- Cold starts: what drives them (runtime, VPC, dependency size) and when they're disqualifying.
- The economics: per-request pricing wins for spiky/low traffic, loses to owned servers at sustained load.

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/articles/serverless.html)

## Archived copy
![[fowler-serverless-clip]]
%% trellis:end %%
