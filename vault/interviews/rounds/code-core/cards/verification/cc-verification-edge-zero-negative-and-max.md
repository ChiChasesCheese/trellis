---
id: cc-verification-edge-zero-negative-and-max
node: verification.edge-catalog
type: qa
---
## Q
What do a zero value, a negative value, and a maximum-sized input each break that a comfortable mid-range value does not?

## A
- **Zero**: `0/0` in a ratio guard; a "has activity" test that is really `count > 0`; a rule firing on an empty group; and presence in the output — a `$0.00` row must still be printed, and must still be there at all.
- **Negative**: a refund or a correction; `//` and `%` change meaning ([[cc-python-pitfalls-negative-floordiv]]); a `min`/`max` seeded with `0` instead of the first element; and a balance that either must be allowed below zero or must not — the statement decides, so re-read it.
- **Maximum**: 10^9-unit amounts and 10^6 rows. Float accumulation drifts, other languages' `int` overflows, and the performance budget is only ever exercised here ([[cc-performance-budget-from-n]]).

## Q zh
零值、负值、最大规模输入，各自会打破哪些「舒适的中段取值」打不破的东西？

## A zh
- **零**：比例守卫里的 `0/0`；名为「是否有活动」实为 `count > 0` 的判断；在空分组上触发的规则；以及是否出现在输出里 —— 一行 `$0.00` 仍然要打印，而且根本不能消失。
- **负数**：一次退款或更正；`//` 和 `%` 的含义会变（[[cc-python-pitfalls-negative-floordiv]]）；用 `0` 而不是首元素初始化的 `min`/`max`；以及一个余额是必须允许为负、还是必须不许 —— 由题面决定，所以回头重读。
- **最大值**：10^9 单位的金额和 10^6 行。浮点累积会漂移，别的语言里 `int` 会溢出，而性能预算只在这里被真正检验（[[cc-performance-budget-from-n]]）。
