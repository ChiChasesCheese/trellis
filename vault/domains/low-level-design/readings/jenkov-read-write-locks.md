---
nodes: [concurrency.primitives]
url: https://jenkov.com/tutorials/java-concurrency/read-write-locks.html
tags: [canonical]
---
# Read / Write Locks in Java (Jakob Jenkov)

A primitive built in front of you: Jenkov implements a read-write lock from
wait/notify in five successive versions, each fixing a real defect — unfair
starvation of writers, then of readers, then reentrance deadlock, then
upgrade/downgrade. Reading it teaches what a mutex, a condition variable and
a fairness policy actually *are*, which is far more useful than a table of
API names.

**Extract on read:**
- The lock/condition mechanism itself: guarded wait in a `while` loop (never
  `if`), signal on state change, and why the loop is mandatory.
- Reentrance is a design decision, not a freebie — the same thread re-entering
  needs explicit bookkeeping or it deadlocks against itself.
- Fairness/starvation: readers can starve writers forever unless the lock
  tracks waiting writers; this is the trade-off to name when you propose a
  read-write lock in an LLD answer.

%% trellis:begin %%
## Source
[Open the original ↗](https://jenkov.com/tutorials/java-concurrency/read-write-locks.html)

## Archived copy
![[jenkov-read-write-locks-clip]]
%% trellis:end %%
