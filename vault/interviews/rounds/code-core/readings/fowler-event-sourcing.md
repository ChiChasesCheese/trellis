---
nodes: [model.event-stream, model.reversal, model.entity-state, model.state-machine]
url: https://martinfowler.com/eaaDev/EventSourcing.html
tags: [canonical]
---
# Event Sourcing (Martin Fowler)

The essay behind almost every "process this stream and report the current state"
problem. State is a fold over an ordered log of events; the current value is
derived, not stored. Fowler works through the two things an assessment then
tests: how you undo an event (a compensating reverse event versus recomputing
from scratch), and what "external updates" do to replayability. Read the
reversal section slowly — it is where charge-and-dispute problems live.

**Extract on read:**
- Derived state versus stored state, and when incremental update is safe
  ([[cc-performance-amortized-incremental-aggregate]]).
- Reversal by a compensating event versus replaying the log without the event —
  and why the two disagree on later events.
- Why the log is the source of truth, which is what makes an out-of-order or
  duplicated event a defined case rather than an accident.

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/eaaDev/EventSourcing.html)

## Archived copy
![[fowler-event-sourcing-clip]]
%% trellis:end %%
