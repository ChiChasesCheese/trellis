---
nodes: [oop.relationships]
url: https://www.uml-diagrams.org/association.html
tags: [reference]
---
# UML Association (uml-diagrams.org)

The precise, spec-accurate answer to "which arrow do I draw?" — association,
shared aggregation, and composite aggregation on one page, each with the
notation, the multiplicity rules, and the lifetime semantics it implies.

**Extract on read:**
- Composite aggregation (filled diamond) means the whole *owns* the part: at
  most one owner, and the parts die with it — the only relationship that
  carries a real lifetime guarantee.
- Shared aggregation (hollow diamond) is deliberately under-specified by the
  spec; if you cannot state the lifetime rule, draw a plain association.
- Navigability arrows and end ownership say who holds the reference (a field
  in the class) — an undirected line means either or both sides may.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.uml-diagrams.org/association.html)

## Archived copy
![[uml-association-clip]]
%% trellis:end %%
