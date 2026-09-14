---
nodes:
- principles.simplicity
title: Unify the declaration, fork the implementation
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0011-decisionmoment-unifies-time-cadence-becomes-constructor
---

# Unify the declaration, fork the implementation

Two models of the same concept can coexist for years — each complete, each well tested, neither aware of the other — because nothing ever forces them to meet. That is a hazard, not untidiness: the canonical example is a firm that lost $440M when a nine-year-old dead code path was reactivated on one of eight servers by a reused flag. Duplicate activation paths and dormant siblings are the same family of risk.

Merging them is a conclusion to be proven, not assumed, because the wrong abstraction costs more than the duplication it replaces. The usable discipline: tabulate the dimensions on which the two models differ and show each one is either absorbed by the merged model or a strict generalization of the old. Here five of six were absorbed and three were generalizations — the new model expressed shapes neither old one could. The sixth difference was recorded as theoretical, with no instance in production, and deliberately not designed for.

The subtler result: inside the merged model, one variant differed on every dimension that mattered — reactive rather than timed, with no meaningful "next occurrence" and no cheap way to evaluate it. The right structure was to unify the declaration layer, where callers only enumerate, and fork the implementation explicitly instead of forcing one path.

Watch, too, for the declarative field with zero consumers: an interface nobody uses is a hypothesis, not a design.
