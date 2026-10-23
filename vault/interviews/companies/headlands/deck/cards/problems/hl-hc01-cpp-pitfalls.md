---
id: hl-hc01-cpp-pitfalls
node: problems.hc01-stock-trading-dp
type: qa
step: 22
---
## Q
用 C++ 写买卖股票 DP，有哪些容易踩的整数与容器陷阱？

## A
1. `i < p.size() - 1`：空输入时 `size()` 为 0，减 1 回绕成 `SIZE_MAX`。
2. `std::vector<...> dp(k + 1)` 且 `k == INT_MAX`：有符号溢出（UB）。
3. `NEG = LLONG_MIN`：`NEG - price` 溢出；应取 `LLONG_MIN / 4`。
4. `(n + 1) * (k + 1)` 用 `int` 算会溢出，格子数用 `long long`。
5. `min_so_far` 取全局最小而不是「之前的最小」。
6. `j` 从小到大更新滚动数组，且 Part 4 买入读了今天的 `idle`。
7. 平局偏向买 / 卖，产生零利润交易或同一天既卖又买。
8. `*opt` 解引用空 `optional` 是 UB，用 `value()`（空时抛异常）。
9. 把 `IllegalState` 继承 `invalid_argument`，一个 `catch` 吞掉两种错误。
10. 用 `int` 存价格差：价格到 2⁴⁰，`int` 装不下。
11. `held` / `idle` 放 `std::array<long long, 2>` 而不是两个 vector：同一 j 的两个数相邻，一次缓存行读写就够，`dp[j]` 与 `dp[j-1]` 也相邻。
