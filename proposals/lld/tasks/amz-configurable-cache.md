# Task: amazon.amz-configurable-cache

- **Leaf id**: `amazon.amz-configurable-cache`   **slug**: `amz-configurable-cache`   **kind**: problem
- **题目**: 可配置缓存（Configurable Cache）
- Instructions: `proposals/lld/PROBLEM_AGENT.md` + `proposals/lld/AMAZON_AGENT.md` (the latter wins).

## What Amazon candidates reported (2026-09-16..10-16 unless noted) — quote at most one sentence per source

- Hello Interview `configurable-cache-design`: 'Design a configurable cache system that supports pluggable eviction policies (e.g., LRU, LFU) and interchangeable storage backends (e.g., in-memory, filesystem, heap, stack).' 2 reports: 2026-09-20 mid-level (LP first half hour: customer pain point; customer asked for an infeasible requirement) and 2026-10-01 senior USA https://www.hellointerview.com/community/questions?company=Amazon (question slug `configurable-cache-design`) [medium–high]
- 1p3a question bank `lru-cache` (onsite/phone, 8 sources, last 2026-10-03); 1p3a 1189999 (2026-09-18 SDE II phone) first question 「要死刘」(= LRU) https://www.1point3acres.com/bbs/thread-1189999-1-1.html [high]

## (reconstructed) — not in any visible report

- what 'heap, stack' storage means for the interviewer (推断: the two axes are eviction policy and storage medium; treat 'heap/stack' as interviewer wording and say so), TTL, stats

## Reuse / link (our own repo first)

- bank [[solution-lru-cache]] (LRU/LFU internals — link) and [[solution-ttl-cache]]
- concept leaves patterns.strategy, patterns.structural (Bridge: two independent axes)

## Card ladder notes

- ladder; step 5 = two axes → composition (Bridge) vs subclass explosion LRUMemoryCache/LFUFileCache…; step 7 = the policy and the store disagree after a failed write
