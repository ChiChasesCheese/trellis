---
nodes: [rules.exact-ratio]
url: https://docs.python.org/3/library/fractions.html
tags: [docs]
---
# fractions — rational numbers

Short page, one idea: exact rational arithmetic with automatic normalization.
It matters when a rule is stated as a ratio — "flag when the fraudulent share
reaches 0.25" — and a float comparison puts the boundary case on the wrong
side. `Fraction("0.25")` is exactly one quarter, and comparing `Fraction(a, b)`
against it is exact. In a hot loop the cross-multiplied integer form is faster;
`Fraction` is the version you can write correctly in ten seconds.

**Extract on read:**
- `Fraction(numerator, denominator)` and `Fraction("0.25")` — construct from a
  string or a pair, never from a float.
- `limit_denominator()` when you must go back to a readable approximation.
- The integer alternative for the same comparison: `a * d >= c * b`, no library
  and no allocation ([[cc-python-pitfalls-float-equality]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/fractions.html)

## Archived copy
![[python-fractions-clip]]
%% trellis:end %%
