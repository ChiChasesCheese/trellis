---
nodes: [patterns.selection]
url: https://gameprogrammingpatterns.com/architecture-performance-and-games.html
tags: [canonical]
---
# Architecture, Performance, and Games (Game Programming Patterns, Bob Nystrom)

The chapter that teaches *refusing* patterns. Nystrom defines good design as
"the cost of change is low", then prices the thing patterns buy you —
decoupling — and shows the bill: more indirection, more files, slower
comprehension, and speculative flexibility for changes that never arrive.
This is the argument to make out loud when an interviewer asks why you did
*not* introduce a factory or a strategy.

**Extract on read:**
- The definition to quote: architecture is good when the next change is
  cheap; abstraction that never absorbs a change was pure cost.
- The three-way tension — flexible vs fast vs done today — and why an
  interview solution sits closer to "done, with named seams" than to fully
  decoupled.
- The over-engineering test: add the abstraction on the *second* concrete
  case, not the first; a pattern applied to a hypothetical is a defect.

%% trellis:begin %%
## Source
[Open the original ↗](https://gameprogrammingpatterns.com/architecture-performance-and-games.html)

## Archived copy
![[gpp-architecture-performance-clip]]
%% trellis:end %%
