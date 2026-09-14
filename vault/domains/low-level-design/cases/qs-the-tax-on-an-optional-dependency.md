---
nodes:
- patterns.structural
title: The tax on an optional dependency, and what a wrapper really is
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0010-nautilus-as-hard-dependency-retire-parallel-abstractions
---

# The tax on an optional dependency, and what a wrapper really is

Making a heavy dependency optional sounds like a kindness to users, but the bill is paid inside the code: lazy class factories that exist only to avoid a top-level import, functions typed as `Any` because the real types may be absent, and a type checker consequently blind in the layer that most needs checking. Those are not designs, they are evasions. Before paying the tax, ask who actually installs without the extra — if CI installs it and every operator installs it, the lightweight path has no consumers and the optionality is pure cost.

Promoting it to a hard dependency then raises a sharper question: which in-house abstractions existed only to hold the vendor at arm's length? The discriminating test is not "this looks duplicated" but "delete it — can the vendor do this natively, and at what cost?"

By that test, a one-way narrowing translation between your model and theirs, with an exhaustive table that raises on an unmapped member, is an anti-corruption layer rather than a duplicate model: one call site, and a new enum member fails loudly instead of mis-mapping a live order. A wrapper interface that lets you support cases the vendor never will is an extension point, not debt. What genuinely must go is two models of one concept, each separately maintained and separately believed.
