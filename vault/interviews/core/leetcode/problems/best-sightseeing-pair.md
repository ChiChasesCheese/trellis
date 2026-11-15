---
slug: best-sightseeing-pair
---
## Q
**LC 1014 最佳观光组合**｜Medium

`values[i]` 是第 `i` 个景点的得分，一对景点 `i < j` 的得分是 `values[i] + values[j] + i - j`（景点间距离会扣分）。求最高的一对得分。

## A
**一句话。** 把式子拆成 `(values[i] + i) + (values[j] - j)`：枚举 `j`，左边取前面 `values[i] + i` 的最大值。

```python
def max_score_sightseeing_pair(values):
    ans = 0
    left = values[0]              # 迄今 max(values[i] + i)
    for j in range(1, len(values)):
        ans = max(ans, left + values[j] - j)
        left = max(left, values[j] + j)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 先更新 `left` 再算答案：`i` 必须严格小于 `j`，要先用旧的 `left` 算 `j` 的答案。
- 初值写成 `0`：`left` 要从 `values[0] + 0` 开始，否则第一个景点被漏掉。

**追问。**
- 同样的拆项思路还见于哪些题？：把依赖两个下标的式子拆成「只含 `i`」与「只含 `j`」两部分，一边维护前缀最优。
- 买卖股票（LC 121）和它的关系？：同样是「前面取最优、当前结算」的一遍扫描。

**同模式。** LC 121 买卖股票的最佳时机、LC 1131 绝对值表达式的最大值、LC 53 最大子数组和
