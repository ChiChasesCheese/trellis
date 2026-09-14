---
nodes: [concurrency.patterns]
url: https://pages.cs.wisc.edu/~remzi/OSTEP/threads-sema.pdf
tags: [canonical, paper]
---
# Semaphores (OSTEP, Arpaci-Dusseau — free chapter)

Every concurrency pattern an LLD round asks for, derived rather than quoted:
binary semaphore as a lock, semaphore as ordering/join, the bounded producer-
consumer buffer built up through three broken versions until it is correct,
the reader-writer lock, and throttling with a counting semaphore. The broken
intermediate versions are the point — each one shows a specific way a naive
blocking queue deadlocks.

**Extract on read:**
- The bounded buffer done right: separate `empty`/`full` counting semaphores
  plus a mutex, and the fatal ordering bug when the mutex is acquired outside
  the counting waits.
- Semaphore as a *rendezvous / ordering* device (initial value 0), not only as
  a lock — this is how a thread pool signals work availability.
- Reader-writer locks and their starvation trade-off, plus counting semaphores
  as an admission-control/throttling knob.

%% trellis:begin %%
## Source
[Open the original ↗](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-sema.pdf)

## Archived copy
![[ostep-semaphores-clip]]
%% trellis:end %%
