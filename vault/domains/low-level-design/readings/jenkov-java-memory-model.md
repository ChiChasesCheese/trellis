---
nodes: [concurrency.model]
url: https://jenkov.com/tutorials/java-concurrency/java-memory-model.html
tags: [canonical]
---
# Java Memory Model (Jakob Jenkov)

The clearest diagram-driven explanation of why multi-threaded code breaks
even when every line looks correct: thread stacks vs heap, CPU caches and
registers holding stale copies, and the two problems that follow —
visibility and race conditions. Language-agnostic in substance; the same
model explains C++, Go, and Python threads.

**Extract on read:**
- Where variables actually live (stack = per-thread, heap = shared) and why a
  written value can sit in a core's cache invisible to everyone else.
- Visibility ≠ atomicity ≠ ordering: `volatile`/happens-before fixes the first,
  synchronization is required for the second, and reordering is legal until
  you forbid it.
- A data race is not "a rare wrong answer" — it is undefined behavior, so
  reasoning about interleavings of racy code is meaningless.

%% trellis:begin %%
## Source
[Open the original ↗](https://jenkov.com/tutorials/java-concurrency/java-memory-model.html)

## Archived copy
![[jenkov-java-memory-model-clip]]
%% trellis:end %%
