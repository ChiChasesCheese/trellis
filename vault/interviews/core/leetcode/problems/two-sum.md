---
slug: two-sum
---
## Q
**LC 1 两数之和**｜Easy

在数组 `nums` 中找两个不同位置的元素，和为 `target`，返回它们的下标（保证恰有一个答案）。

## A
**一句话。** 哈希表存「值→下标」，一遍扫描时先查 `target - x` 是否出现过，再存 `x`。

```python
def two_sum(nums, target):
    seen = {}                    # 值 -> 下标
    for i, x in enumerate(nums):
        j = seen.get(target - x)
        if j is not None:        # 先查，只会配到前面的元素
            return [j, i]
        seen[x] = i              # 后存，不会自己配自己
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先存后查：`[3,2,4]`、`target=6` 返回 `[0,0]`（`3` 用了两次）。
- 写成 `if j:`：下标 `0` 被当成没找到，`[2,7]`、`9` 返回空。

**追问。**
- 数组已有序（LC 167）？：左右双指针，`O(n)` 时间 `O(1)` 空间。
- 要返回所有不重复的数值对？：用 `Counter`，`x` 与 `target-x` 相同时要求至少出现两次。

**同模式。** LC 167 两数之和 II、LC 15 三数之和、LC 653 两数之和 IV、LC 560 和为 K 的子数组
