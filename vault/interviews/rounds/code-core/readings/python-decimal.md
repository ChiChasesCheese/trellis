---
nodes: [python.stdlib, rules.money, rules.rounding, rules.tiers]
url: https://docs.python.org/3/library/decimal.html
tags: [docs]
---
# decimal — decimal fixed point and floating point arithmetic

The reference for exact money arithmetic, and the page that states plainly what
most candidates get wrong: constructing a `Decimal` from a float inherits the
float's error, and the default rounding mode is `ROUND_HALF_EVEN`, not the
half-up that specifications usually mean. The FAQ at the bottom answers the two
practical questions — how to round to cents, and how to keep a fixed number of
decimal places through a chain of operations.

**Extract on read:**
- `Decimal("0.029")` from a string; `quantize(exp, rounding=ROUND_HALF_UP)` as
  the one place rounding happens ([[cc-python-stdlib-decimal-calls]]).
- The rounding-mode table: half-even vs half-up vs floor vs `ROUND_DOWN`.
- `getcontext().prec` — precision is significant digits, not decimal places,
  and that distinction bites on large amounts.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/decimal.html)

## Archived copy
![[python-decimal-clip]]
%% trellis:end %%
