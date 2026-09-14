---
nodes: [principles.composition]
url: https://python-patterns.guide/gang-of-four/composition-over-inheritance/
tags: [canonical]
---
# The Composition Over Inheritance Principle (Brandon Rhodes)

The single best explanation of *why* deep hierarchies rot: it walks a logging
example into a subclass explosion, then dissolves it four different ways
(adapter, bridge, decorator, plain composition), comparing each.

**Extract on read:**
- The m×n subclass-explosion argument: each new axis of variation multiplies
  the hierarchy; composition keeps the axes independent.
- "Inheritance is a mechanism for sharing implementation; composition is a
  mechanism for delegating responsibility" — delegation as the default.
- When inheritance still wins: a genuine is-a with a stable base contract and
  one axis of variation.

%% trellis:begin %%
## Source
[Open the original ↗](https://python-patterns.guide/gang-of-four/composition-over-inheritance/)

## Archived copy
![[python-patterns-composition-clip]]
%% trellis:end %%
