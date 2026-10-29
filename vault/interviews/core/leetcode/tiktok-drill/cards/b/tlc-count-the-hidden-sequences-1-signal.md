---
id: tlc-count-the-hidden-sequences-1-signal
node: b.count-the-hidden-sequences
type: qa
step: 1
---
## Q
**LC 2145 统计隐藏数组数目**｜Medium · LC TikTok 热度 62/100

长度为 `n` 的 `differences` 是隐藏数组 `hidden`（长度 `n + 1`）的相邻差：`differences[i] = hidden[i + 1] - hidden[i]`。`hidden` 的所有元素都在 `[lower, upper]` 内。返回满足条件的 `hidden` 的个数。`1 <= n <= 10^5`，`-10^5 <= differences[i] <= 10^5`，`-10^5 <= lower <= upper <= 10^5`。例：`[1,-3,4]`，`[1,6]` → `2`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「已知相邻差，求原数组」→ 差分的逆运算是**前缀和**：`hidden[i] = hidden[0] + prefix[i]`。
- 数组由起点唯一确定，只有一个自由度 → 问题化为“起点有几种取法”。
- 「所有元素都在 `[lower, upper]`」→ 只和**最大值与最小值**有关，不用逐个检查。
- `n = 10^5`，值域 `2 × 10^5` → 枚举起点再逐个检查是 `O(n · 值域)`，太慢；要 `O(n)`。
- 前缀和要包含起点自己（偏移 `0`）。

**推导链。**
1. 暴力：枚举起点 `x ∈ [lower, upper]`，逐个检查 `x + prefix[i]` 是否都在区间内。
2. 浪费：每个起点都重检整条序列，而序列的形状（相对起点的偏移）是固定的。
3. 洞察：合法 ⇔ `x + min(prefix) >= lower` 且 `x + max(prefix) <= upper`，即 `x ∈ [lower - min, upper - max]`。
4. 最优：个数 = `max(0, (upper - lower) - (max - min) + 1)`，一次前缀和，`O(n)`。

**同模式的题**：LC 303 区域和检索、LC 1094 拼车、LC 370 区间加法、LC 53 最大子数组和。
