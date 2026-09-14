---
nodes:
- principles.solid
title: When a low layer needs a high layer's type, sink the type
codebase: quant-stroller
ref: 4dae805d2955
artefact: contracts:.importlinter#forbid-data-to-experiment
---

# When a low layer needs a high layer's type, sink the type

A low-level module needs a type defined in a high-level one — a result object, an enum, an error class. Three moves are available: import upward (creating a cycle and inverting the layering), copy the definition (two models of one concept, guaranteed to drift), or sink the shared type into a neutral module both sides may depend on.

The third is the dependency-inversion principle in its most mundane form. Dependencies should point toward stability, and shared vocabulary is more stable than either party that uses it. The refactoring trigger to watch for is precisely this shape: a stable, widely-used module reaching up into a volatile one for a definition.

Having performed the move, add the forbidden edge as a contract, so the regression cannot return the next time someone is in a hurry — otherwise the fix survives only as long as the memory of it.

The failure mode of doing this repeatedly is a core package that everything imports and that therefore can never change. Keep it to types and pure functions with no dependencies of its own, and treat behaviour migrating into it as a warning. The signal that you sank the wrong thing is the core module starting to import back out.
