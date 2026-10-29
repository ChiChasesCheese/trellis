---
id: tlc-nge-tou-zi-de-dian-shu-lcof-4-followup
node: b.nge-tou-zi-de-dian-shu-lcof
type: qa
step: 4
---
## Q
**剑指 Offer 60 n个骰子的点数**｜追问

面试官接着问：（1）骰子换成 `k` 面的呢？（2）只想知道「点数和至少为 `T`」的概率？（3）每格要加 6 项，能不能更快？空间呢？

## A
1. **`k` 面骰子**：内层改成 `range(1, k + 1)`，表宽变成 `k·num + 1`，和的范围 `[num, k·num]`。时间 `O(k^2 · num^2)`（`num · k·num` 格，每格 `k` 项）。
2. **和至少为 `T`**：对概率数组做后缀和。`list(accumulate(reversed(probs)))[::-1]` 得到「和 ≥ 第 `i` 小的值」的概率，下标仍要减去 `num` 平移。
3. **更快**：`dp[i][j]` 是上一行 `dp[i-1][j-6 .. j-1]` 这一段的和，先算上一行的前缀和 `pre = list(accumulate(dp[i-1], initial=0))`，每格变成 `pre[j] - pre[max(0, j - 6)]`，与 `k` 无关，时间降到 `O(k · num^2)`。空间可以压到 `O(num)`：见 Python 工具箱「DP 降维」。

**Python 提醒**：列表的负下标是合法的，`row[-1]` 是最后一个元素；DP 里 `j - face` 算出负数时不会抛 `IndexError`，只会悄悄读错数，所以边界条件要显式写出来。
