---
slug: successful-pairs-of-spells-and-potions
---
## Q
**LC 2300 咒语和药水的成功对数**｜Medium

`spells[i] * potions[j] >= success` 即为一对成功，求每个咒语能配成功的药水数量。

## A
**一句话。** 药水排序一次，对每个咒语二分找第一个满足乘积达标的位置，其右边全部成功。

```python
def successful_pairs(spells, potions, success):
    potions = sorted(potions)
    m = len(potions)
    return [m - bisect_left(potions, success,
                            key=lambda p: p * s)
            for s in spells]
```

**复杂度。** 时间 `O((n+m) log m)`，空间 `O(m)`。

**易错点。**
- 用 `bisect_right`：恰好等于 `success` 的组合被漏掉，`([2], [8,8], 16)` 得 `0`，应为 `2`。
- 用 `success // s` 向下取整当下限：`([2], [3,4], 7)` 得 `2`，应为 `1`（`2*3 < 7`）；要向上取整。
- 忘了排序药水：无序数组上二分没有意义。

**追问。**
- 还能更快吗？：咒语也排序，用双指针，咒语变大时成功个数只增不减。
- 药水值域只有 `10^5`？：计数数组加后缀和，每个咒语 `O(1)` 查 `suffix[ceil(success/s)]`。

**同模式。** LC 1498 满足条件的子序列数目、LC 475 供暖器、LC 744 寻找比目标字母大的最小字母、LC 2389 和有限的最长子序列
