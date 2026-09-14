---
nodes: [python.pitfalls, rules.money, rules.thresholds, input.numbers]
url: https://docs.python.org/3/tutorial/floatingpoint.html
tags: [docs, canonical]
---
# Floating Point Arithmetic: Issues and Limitations

Fifteen minutes that permanently fix the intuition behind a whole class of
failed hidden tests. It shows why `0.1` is not `0.1`, why `0.1 + 0.2 == 0.3` is
`False`, and — the section people skip — why the error is not "tiny and
harmless" once you accumulate it over a million rows or compare it against a
threshold. It ends with `math.fsum`, `Fraction` and `Decimal` as the three
principled escapes.

**Extract on read:**
- Representation error versus accumulated error: two distinct bugs with two
  distinct fixes ([[cc-python-pitfalls-float-equality]]).
- Why exact equality on floats is never the right test, and what `math.isclose`
  is actually for.
- `float` holds integers exactly only up to 2^53 — the boundary that matters
  when amounts are large.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/tutorial/floatingpoint.html)

## Archived copy
![[python-floating-point-clip]]
%% trellis:end %%
