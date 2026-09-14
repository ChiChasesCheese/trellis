---
nodes:
- principles.coupling
title: 'Independence: neither side may know the other'
codebase: quant-stroller
ref: 4dae805d2955
artefact: contracts:.importlinter#alpha-broker-independent
---

# Independence: neither side may know the other

Layering says a dependency may point one way. Independence is the stronger claim that two subsystems may not know about each other in *either* direction. It is worth paying for when both must be substitutable and separately testable: the decision-making side can be exercised with no external system in sight, and a new external system can be added without touching a single decision module.

The mechanism is a contract that fails the build on any import path between the two packages, in either direction — not a review habit, because the violating import is always locally convenient and globally expensive.

The cost lands immediately on shared vocabulary. Two modules that must not see each other still need to agree on what an order, an identifier, or a result is, so those definitions must move down into a common module, and that module tends to accumulate. Independence also removes the shortcut symmetrically: the execution side cannot peek at the logic that produced a target, so everything it needs must travel in the message.

Choose independence where the boundary is a genuine substitution point. Where one side is honestly built on the other, a one-way layer rule says so and costs less.
