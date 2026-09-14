---
nodes: [structure.api, structure.storage, concurrency.patterns, concurrency.primitives]
tags: [classic, medium]
---
# Drill: LRU Cache (then make it thread-safe)

Code an LRU cache with O(1) get/put; then the follow-up every interviewer
holds in reserve: make it safe under concurrent access without killing
throughput.

**Constraints to state and honor**
- O(1) both operations; capacity eviction; generic keys/values.
- Phase 2: correct under concurrent get/put; discuss lock granularity.
- Phase 3 (stretch): TTL expiry — where does the clock live for testability?

**Grading points**
- Hash map + doubly-linked list invariants stated before coding — [[structure.api|In-Process API Design]].
- Encapsulating the list surgery so eviction can't be half-done — [[structure.storage|In-Memory Persistence]].
- Coarse lock first, then reasoned refinement (segment/striped locks; read-write lock is a trap here — gets mutate order) — [[concurrency.primitives|Synchronization Primitives]].
- Injected clock for TTL tests — [[concurrency.patterns|Concurrency Patterns]].

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):
