---
nodes: [structure.state-machines, patterns.behavioral, method.delivery, concurrency.hazards]
tags: [classic, medium]
---
# Drill: Elevator System

Design and code an N-elevator controller: floor requests, car requests,
scheduling, door lifecycle.

**Constraints to state and honor**
- Elevator lifecycle is an explicit state machine (idle/moving-up/moving-down/doors-open); no boolean soup.
- Scheduling policy swappable (nearest-car vs SCAN); must add a new policy without touching the controller.
- Requests arrive concurrently from every floor.

**Grading points**
- State machine as enum + transition table — [[structure.state-machines|State Machines]].
- Scheduler as strategy; observer for floor-panel updates — [[patterns.behavioral|Behavioral Patterns]].
- Scoping discipline: single elevator first, N elevators only after core works — [[method.delivery|Round Structure]].
- Request queue synchronization; no deadlock between controller and car threads — [[concurrency.hazards|Deadlock & Friends]].

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
