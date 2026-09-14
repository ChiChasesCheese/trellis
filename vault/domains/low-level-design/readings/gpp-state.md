---
nodes: [structure.state-machines]
url: https://gameprogrammingpatterns.com/state.html
tags: [canonical]
---
# State (Game Programming Patterns, Bob Nystrom)

The best free explanation of state machines anywhere: starts from the boolean
soup a character controller becomes, derives FSMs, the State pattern, then
pushdown automata and hierarchical machines — exactly the ladder an elevator
or order-lifecycle problem climbs.

**Extract on read:**
- The derivation: flag combinations → enum + switch → one class per state;
  each step's cost and when the simpler one is enough.
- Transitions live in the states (or a table), entry/exit actions replace
  scattered setup code, and illegal transitions become unrepresentable.
- Static states vs instantiated states, and pushdown automata for
  "return to previous state" requirements.

%% trellis:begin %%
## Source
[Open the original ↗](https://gameprogrammingpatterns.com/state.html)

## Archived copy
![[gpp-state-clip]]
%% trellis:end %%
