---
id: tlc-tt-currency-conversion-queries-3-why
node: p4.tt-currency-conversion-queries
type: qa
step: 3
---
## Q
**货币兑换查询**｜正确性

带权并查集里 `ratio[x]` 表示 `1` 个 `x` 兑换成多少个根货币。合并时为什么新的比率是 `rate · ratio[b] / ratio[a]`？路径压缩时为什么顺序和乘法都不能错？未知货币不判断、压缩只改 `parent` 不改 `ratio`、递归的 `find`，各会错成什么样？

## A
**不变量。** 对每个货币 `x`，`ratio[x]` 满足：`1` 个 `x` 等于 `ratio[x]` 个 `parent[x]`；顺着 `parent` 链把比率连乘，就是 `1` 个 `x` 兑换成根的个数。合并 `1 a = rate b`：设 `1 a = ratio[a] ra`、`1 b = ratio[b] rb`（`find` 之后 `a`、`b` 已直连各自的根），则 `ratio[a] ra = rate · ratio[b] rb`，所以 `1 ra = rate · ratio[b] / ratio[a]` 个 `rb`，这就是挂上去的那条边的权。查询时同一集合内 `1 a = ratio[a] root`、`1 b = ratio[b] root`，所以 `1 a = ratio[a] / ratio[b]` 个 `b`。

**反例一：未知货币不判断。** 查询 `("USD", "GBP")` 而 `GBP` 从未出现过，直接 `parent["GBP"]` 抛 `KeyError`；先判断是否在 `parent` 里，返回 `-1.0`。

**反例二：压缩只改 `parent`、不乘 `ratio`。** 链 `A -> B -> C`（`A` 的父亲是 `B`，`B` 的父亲是根 `C`），压缩后 `A` 直连 `C`，但 `ratio[A]` 仍是 `A` 到 `B` 的比率，查询 `A` 到 `C` 的结果少乘了 `B` 到 `C` 的那一段。比如 `1 A = 2 B`、`1 B = 3 C`，正确 `ratio[A]` 要变成 `6`，不改就是 `2`。

**反例三：递归的 `find`。** 汇率形成长度 `10^5` 的链，`find` 递归到约 `1000` 层就 `RecursionError`；用循环收集路径再压缩，深度不再成问题。

**反例四：压缩顺序反了。** 从离叶子最近的一端开始压缩，此时它的父亲还没有直连根，乘上的是“到旧父亲”的比率，结果少了一段；必须从靠近根的一端往下处理（`reversed(path)`）。
