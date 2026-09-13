---
nodes: [content.isr, caching.validators, caching.invalidation, caching.stampede, distributed.cross-region]
tags: [nextjs, flagship]
---
# Drill: Design global ISR serving

Design the serving and regeneration path for 20 million product pages using
Incremental Static Regeneration (ISR).

**Constraints to state and honor**
- The hottest 1% of pages receive 80% of traffic.
- Price changes require on-demand revalidation across 20 regions.
- The rendering function sometimes takes 8 seconds or fails.
- A deployment can be rolled back while regeneration is in progress.

**Grading points**
- Build-time artifacts versus on-demand generation and durable ISR storage.
- Fresh, stale, and missing states; stale-while-revalidate and stale-if-error behavior.
- Per-key request collapsing and protection against regional stampedes.
- Versioned metadata and atomic invalidation of HTML plus associated data payloads.
- Cross-region propagation contract, observable staleness, and rollback semantics.
- Cost model for function invocations, cache reads and writes, and origin transfer.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):

