---
id: tlc-maximum-value-at-a-given-index-in-a-bounded-array-4-followup
node: a.maximum-value-at-a-given-index-in-a-bounded-array
type: qa
step: 4
---
## Q
**LC 1802 有界数组中指定下标处的最大值**｜追问

面试官接着问：（1）能不能用标准库的二分，不手写循环？（2）能不能不二分，直接 `O(1)` 求解？（3）如果相邻差的上限是 `d` 而不是 `1`？

## A
1. **`bisect` 的 `key`**：`total(v)` 对 `v` 单调不减，范围 `1..max_sum` 可以用 `range` 当序列，Python 3.10+ 的 `bisect_right(a, x, key=...)` 返回满足 `key(a[i]) <= x` 的元素个数，也就是满足 `total(v) <= max_sum` 的 `v` 的个数。因为可行的 `v` 恰好是 `1..答案`，个数就是答案：`bisect_right(range(1, max_sum + 1), max_sum, key=total)`。`range` 不占内存，`key` 只在被访问到的位置计算，所以仍是 `O(log max_sum)`。
2. **`O(1)`**：`total(v)` 在两个区域是关于 `v` 的二次函数（降到 `1` 之前 / 之后），分段解一元二次不等式，再取整数根。能做，但边界很多，容易出错，面试里二分更稳。
3. **差值上限 `d`**：每格最多降 `d`，等差数列的公差变成 `d`：一侧前 `t = ceil((peak - 1) / d)` 格是递减的，之后补 `1`，`side` 里的项数与求和公式相应调整，二分框架不变。

**Python 提醒**：`bisect` 的 `key=` 参数从 Python 3.10 开始支持；它不会预先计算整个序列，只在比较时调用 `key`。整数除法 `//` 在两个正整数上向下取整；`(a + b + 1) // 2` 是上取整的中点，二分“最大可行”时必须用它。
