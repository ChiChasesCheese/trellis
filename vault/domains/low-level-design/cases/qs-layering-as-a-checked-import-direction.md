---
nodes:
- principles.coupling
title: Layering is a claim about import direction — check it or lose it
codebase: quant-stroller
ref: 4dae805d2955
artefact: contracts:.importlinter#module-graph-tiers
---

# Layering is a claim about import direction — check it or lose it

A layered design is a claim about which direction imports may point, and a claim that lives only in a diagram decays within weeks. Encoding the tiers as a machine-checked contract — a higher tier may import a lower one, never the reverse — turns the diagram into a build failure.

Two wrinkles appear once you try it. First, a checker that walks every package treats same-tier packages as independent siblings and will happily allow one to import another, quietly re-creating the tangle the layering was meant to prevent; declaring one representative package per tier as a spine keeps the check meaningful. Second, imports that exist only for type annotations are not runtime dependencies, so excluding them keeps the graph honest instead of forcing fake indirection just to satisfy a linter.

The cost is real. Legitimate shortcuts become illegal, exceptions accumulate as an explicit ignore list, and every entry on that list is a small lie you have chosen to keep visible. What you buy is architecture that is falsifiable: a newcomer — or a code-generating agent that never read your wiki — learns the boundary from a failing check in seconds rather than from a reviewer's memory.
