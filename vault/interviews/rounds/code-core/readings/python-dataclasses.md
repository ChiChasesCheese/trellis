---
nodes: [python.classes, model.records]
url: https://docs.python.org/3/library/dataclasses.html
tags: [docs]
---
# dataclasses — data classes

The cheapest way to get a record with a readable `__repr__`, structural
equality and, optionally, ordering — all of which you would otherwise hand-write
while the clock runs. Read the decorator's parameter list carefully: `order`,
`frozen`, `eq`, `slots` and `kw_only` each change what the generated class can
do, and `field(compare=False, default_factory=...)` is where the per-field
control lives.

**Extract on read:**
- `order=True` compares fields in declaration order, so declaration order is the
  sort order ([[cc-python-classes-dataclass-ordering]]).
- Why a mutable default raises at class creation, and `default_factory` as the
  fix ([[cc-python-classes-default-factory]]).
- `frozen=True` gives hashability; `slots=True` removes the per-instance dict
  ([[cc-python-classes-slots]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/dataclasses.html)

## Archived copy
![[python-dataclasses-clip]]
%% trellis:end %%
