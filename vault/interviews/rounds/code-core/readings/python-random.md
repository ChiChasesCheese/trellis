---
nodes: [verification.determinism, transfer.quant]
url: https://docs.python.org/3/library/random.html
tags: [docs]
---
# random — generate pseudo-random numbers

Read it for reproducibility, not for randomness. The page documents that
`random` is a module-level instance of `random.Random`, which is why seeding it
globally is fragile: any import or any other test can advance the same
generator. Creating your own `random.Random(0)` gives an independent stream that
a failing case can be replayed from. The distribution functions at the bottom
are what you reach for when a question asks you to simulate rather than derive.

**Extract on read:**
- `rng = random.Random(0)` as an instance, versus `random.seed(0)` as global
  state ([[cc-verification-determinism-seeded-random]]).
- `choices(population, weights=...)`, `sample`, `shuffle`, `gauss` — the
  simulation primitives ([[cc-transfer-quant-simulate-vs-closed-form]]).
- The explicit warning that this generator is not suitable for security, and
  `secrets` is.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/random.html)

## Archived copy
![[python-random-clip]]
%% trellis:end %%
