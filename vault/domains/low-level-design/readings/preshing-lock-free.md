---
nodes: [concurrency.primitives]
url: https://preshing.com/20120612/an-introduction-to-lock-free-programming/
tags: [canonical]
---
# An Introduction to Lock-Free Programming (Jeff Preshing)

The reference map of the lock-free world, and the counterweight to the
lock-based half of this leaf: what "lock-free" actually means (progress
guarantee, not "no mutex"), read-modify-write and compare-and-swap, the
CAS retry loop, ABA, and why memory ordering is inseparable from it.

**Extract on read:**
- Lock-free = some thread always makes progress; a suspended thread can never
  block the rest. It is a *guarantee*, not an optimization claim.
- The CAS loop shape — read, compute, compare-and-swap, retry — and the ABA
  problem it silently hides.
- Sequential consistency vs the reordering the compiler and CPU are allowed to
  do: atomics need explicit ordering, which is why "just make it atomic" is
  usually wrong.

%% trellis:begin %%
## Source
[Open the original ↗](https://preshing.com/20120612/an-introduction-to-lock-free-programming/)

## Archived copy
![[preshing-lock-free-clip]]
%% trellis:end %%
