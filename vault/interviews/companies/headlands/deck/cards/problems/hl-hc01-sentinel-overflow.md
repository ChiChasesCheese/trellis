---
id: hl-hc01-sentinel-overflow
node: problems.hc01-stock-trading-dp
type: qa
step: 7
---
## Q
股票 DP 里不可达状态的哨兵值（sentinel）为什么取 `Long.MIN_VALUE / 4`？入口为什么限制价格上界、天数上界？

## A
**哨兵值**：有些状态一开始不可达（没买过，不可能 `HOLD`），给它一个极小的数，`max` 自动忽略。如果直接用 `Long.MIN_VALUE`，再 `- price` 会**下溢**绕回成巨大正数，反而被当成最优；`NEG = Long.MIN_VALUE / 4` 留足余量，`NEG + 价格` 仍极负。

**从源头消灭溢出**：入口规定 `0 ≤ price ≤ 2⁴⁰ = MAX_PRICE`、`n ≤ 2²² = MAX_DAYS`。最多 n/2 笔交易，利润 ≤ 2²¹ × 2⁴⁰ = 2⁶¹ < 2⁶³，`long` 里任何中间值都不溢出，内循环不用写 `Math.addExact`。入口检查一次比热路径检查百万次便宜；「拒绝」也比「静默回绕」安全。校验失败：`null` → `NullPointerException`（`Objects.requireNonNull`），越界 → `IllegalArgumentException`。

利润用 `int` 累加会溢出；价格上界附近（`0, 2⁴⁰, 0, 2⁴⁰ …` 共 1000 笔）是测试专打的边界。
