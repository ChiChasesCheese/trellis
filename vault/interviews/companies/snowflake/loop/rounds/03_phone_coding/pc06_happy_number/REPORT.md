# pc06 Happy Number — report

## Summary
2026 夏一手：项目讨论约 20 分钟后，Happy Number 先 O(n) 再被要求 O(1)。3-part：Part 1 集合判环 → Part 2 Floyd 快慢指针（一手原追问）→ Part 3 推广到任意进制与幂次并报告环长与环中最小值 **(reconstructed)**。

## Sources & confidence
HIGH（1p3a thread-1179571 / t.me 28738 摘要，题目与"优化到 O(1)"均为原文）；Part 3 为重建。

## Approach by part
1. `seen` 集合，直到 `n == 1` 或重复。
2. `slow = n, fast = f(n)`；`slow` 走一步、`fast` 走两步，直到 `fast == 1` 或相遇；返回 `fast == 1`。无容器。
3. 同样用 Floyd 在 `f_{base,power}` 上找到环内一点，再绕环一圈数长度并记最小值；O(1) 额外空间。

## Pitfalls hidden tests target
- Part 2 偷用 `set` / `dict`：测试把模块全局的 `set`、`dict` 替换为报错函数（模块全局名遮蔽内置名）
- Part 2 峰值内存上限（tracemalloc，1–2000 连续调用 < 16 KB）
- `n = 1`、`10^300`、`n ≤ 0`
- Part 3：自反点、二进制退化、非法 base/power
- Part 2 与 Part 1 在 1–3000 与 2000 个随机 ≤ 10^18 的数上结果一致

## Complexity & measured cost
每次 `f` 是 O(位数)；进环前的尾巴与环长在十进制平方和下都很短（环长 8）。编排者验证：1–200000 上集合法与 Floyd 0 不一致；Part 3 与"字典记录首次出现位置"的暴力找环在 3000 组（base 2–16、power 1–4）上 0 不一致。perf：10^5 个 ≤ 10^12 的查询端到端 < 2 s。

## Test inventory
25 tests — part1 9（含 5 参数化、1 io）· part2 11（含 5 参数化、1 perf、1 io）· part3 4（含 1 io/fmt）；edge 10 · fmt 1 · perf 1 · io 3。

## Skills exercised
S08 复杂度再压一档（Floyd 判环）· S05 隐式图 / 链表判环
