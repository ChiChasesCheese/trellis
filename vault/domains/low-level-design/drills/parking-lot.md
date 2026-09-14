---
nodes: [method.modeling, oop.relationships, patterns.creational, structure.storage]
tags: [classic, easy]
---
# Drill: Parking Lot

The canonical warm-up. Design and code a parking lot: multiple floors,
spot types (compact/large/handicapped/EV), ticketing, fee calculation.

**Constraints to state and honor**
- Nearest-available-spot assignment per vehicle type; EV spots have chargers.
- Fee strategies differ by vehicle type and duration; must be swappable.
- Entry/exit panels operate concurrently.

**Grading points**
- Entities vs value objects (Ticket vs Money) — [[method.modeling|Requirements to Objects]].
- Spot-type/vehicle-type matching without instanceof ladders — [[oop.relationships|Class Relationships]].
- Fee calculation as a strategy; spot allocation as a swappable policy — [[patterns.creational|Creational Patterns]].
- Thread-safe spot assignment (two gates, one spot) — [[structure.storage|In-Memory Persistence]].

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
