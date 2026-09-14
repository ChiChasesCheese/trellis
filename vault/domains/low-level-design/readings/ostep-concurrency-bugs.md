---
nodes: [concurrency.hazards]
url: https://pages.cs.wisc.edu/~remzi/OSTEP/threads-bugs.pdf
tags: [canonical, paper]
---
# Common Concurrency Problems (OSTEP, Arpaci-Dusseau — free chapter)

The definitive free treatment of concurrency hazards, and it opens with a
study of real bugs found in MySQL, Apache, Mozilla and OpenOffice: about
two-thirds are non-deadlock (atomicity and order violations) and one-third
deadlock. Then the full deadlock theory with the four conditions and one
concrete breaker for each — exactly the checklist to recite when an
interviewer asks "could this deadlock?".

**Extract on read:**
- The four necessary conditions — mutual exclusion, hold-and-wait, no
  preemption, circular wait — and the practical breaker for each (lock-free
  primitives, atomic acquire-all, trylock+backoff, total lock ordering).
- Total lock ordering by address is the trick that makes `transfer(a, b)`
  correct without a global lock.
- Non-deadlock bugs dominate in practice: atomicity violations (a check and
  its use split across a lock boundary) and order violations (assuming
  initialization already ran).

%% trellis:begin %%
## Source
[Open the original ↗](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-bugs.pdf)

## Archived copy
![[ostep-concurrency-bugs-clip]]
%% trellis:end %%
