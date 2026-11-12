---
slug: minimum-increment-to-make-array-unique
---
## Q
**LC 945 使数组唯一的最小增量操作**｜Medium

每次操作可把某个元素加 `1`。求让 `nums` 中所有值互不相同的最少操作次数。

## A
**一句话。** 排序后从小到大扫，每个数至少抬到「前一个占用的值 + 1」。

```python
def min_increment_for_unique(nums):
    moves = 0
    nxt = 0                    # 下一个没被占用的最小值
    for x in sorted(nums):
        t = max(x, nxt)
        moves += t - x
        nxt = t + 1
    return moves
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 不排序直接贪心：`[3,2,1,2,1,7]` 得 `17`，应为 `6`。
- `nxt` 更新成 `x + 1`：`[1,1,1]` 得 `2`，应为 `3`（要用抬完后的 `t + 1`）。

**追问。**
- 允许加也允许减、代价是 `|变化量|`？：斜率技巧（slope trick），用大根堆维护。
- 值域很小怎么更快？：计数排序，一遍扫值域，把多余的个数往后推，`O(n + 值域)`。

**同模式。** LC 1827 最少操作使数组递增、LC 1647 字符频次唯一的最小删除次数、LC 135 分发糖果
