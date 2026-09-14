---
nodes: [caching.keys, delivery.flags, delivery.shadow, delivery.canary, delivery.rollback, security-cost.poisoning]
tags: [rollout, correctness]
---
# Drill: Roll out a cache-key change

A proposed cache-key algorithm normalizes query parameters and reduces estimated
storage by 18%. Roll it out without serving one tenant's content to another.

**Constraints to state and honor**
- Production has billions of existing objects under the old key.
- Some origins vary on undocumented headers.
- Cache-hit ratio and storage improve slowly; a correctness leak is immediately severe.
- The new implementation exists in both Lua and Go.

**Grading points**
- Explicit key contract and inventory of every input that can alter the response.
- Shadow computation without writes or side effects; divergence classification.
- Cohort selection, deployment-version labels, and 1-10-50-100 progression.
- Correctness guardrails separate from performance and cost metrics.
- Stop conditions, kill switch, dual-read or fallback strategy, and cache cleanup.
- How to prove Lua and Go normalization stay byte-for-byte compatible.

**Attempt log**
- [ ] Attempt 1 (date, 30 min, self-graded notes):

