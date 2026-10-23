---
id: hl-c16-trap-midpoint-division
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 14
---
## Q
二分的中点怎么写才不溢出？`7/2`、`-7/2`、`-7%3`、`1999/100` 在 C++ 里各是多少？金额怎么存？

## A
- 中点：`int mid = lo + (hi - lo) / 2;`。`(lo + hi) / 2` 在 `lo = 2'000'000'000, hi = 2'100'000'000` 时溢出 `int`（UB）；安全写法得 2050000000。
- 整数除法**向零截断**：`7/2 = 3`，`7.0/2 = 3.5`，`-7/2 = -3`；`%` 保留**被除数的符号**：`-7%3 = -1`。
- `double dollars = cents / 100;` 先做整数除法得 19；要写 `cents / 100.0` 得 19.99。
- 金额用**整数分**（`long`），不要用 `double`。
