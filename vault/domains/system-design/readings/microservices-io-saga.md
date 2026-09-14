---
nodes: [correctness.saga]
url: https://microservices.io/patterns/data/saga.html
tags: [canonical]
---
# Saga (microservices.io, Chris Richardson)

The reference description of sagas from the author of *Microservices
Patterns*: a sequence of local transactions coordinated by events
(choreography) or an orchestrator, with compensating transactions instead
of rollback. The one page to internalize before any "book a trip" question.

**Extract on read:**
- Choreography vs orchestration, and why orchestration wins as steps grow.
- Compensating transactions: semantic undo, not rollback — some steps (email sent) can't compensate.
- Sagas are ACD without I: countermeasures for the isolation you gave up (semantic locks, pending states).

%% trellis:begin %%
## Source
[Open the original ↗](https://microservices.io/patterns/data/saga.html)

## Archived copy
![[microservices-io-saga-clip]]
%% trellis:end %%
