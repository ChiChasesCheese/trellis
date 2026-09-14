---
nodes: [patterns.creational]
url: https://refactoring.guru/design-patterns/builder
tags: [canonical]
---
# Builder (refactoring.guru)

The one creational pattern page worth reading end to end: it starts from the
telescoping-constructor mess every machine-coding problem produces (a Pizza,
a Report, a Query with fifteen optional fields), derives the builder step by
step, and ends with the director/fluent variants and the honest trade-offs.
Read this once and the rest of the creational family (factory method,
abstract factory, prototype) reads as variations on "who decides what to
construct".

**Extract on read:**
- The trigger: a constructor with many optional parameters, or subclasses
  created only to cover parameter combinations — that's the smell builder cures.
- Builder returns a *validated, complete* object; the invariant check belongs
  in `build()`, not spread over setters.
- The Relations section: builder vs abstract factory vs prototype — which one
  the interviewer means when they say "make object creation flexible".

%% trellis:begin %%
## Source
[Open the original ↗](https://refactoring.guru/design-patterns/builder)

## Archived copy
![[refactoring-guru-builder-clip]]
%% trellis:end %%
