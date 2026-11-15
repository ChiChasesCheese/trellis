---
slug: sorting-three-groups
---
## Q
**LC 2826 将三个组排序**｜Medium

数组 `nums` 只含 1、2、3，每次可删一个元素，求变成非递减的最少删除数。

## A
**一句话。** 删得最少 = 留下最长非递减子序列；值只有三种，`best[v]` 记「末尾 `<= v` 时最多保留几个」，每来一个数更新 `v >= x` 的状态。

```python
def minimum_operations(nums):
    best = [0] * 4      # best[v]：末尾 <= v 时最长保留
    for x in nums:
        keep = best[x] + 1          # 接在末尾 <= x 的后面
        for v in range(x, 4):
            best[v] = max(best[v], keep)
    return len(nums) - best[3]
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 当成严格递增：`[2,2,2]` 不用删，状态要「`<= v`」而不是「`< v`」。
- 只更新 `best[x]`：末尾为 `x` 的序列也算「末尾 `<= 3`」，`v > x` 的状态要一起抬高。

**追问。**
- 值域很大？：就是最长非递减子序列，贪心加 `bisect_right`，`O(n log n)`。
- 状态机写法？：`f1, f2, f3` 表示最后一段是 1、2、3 时的最少删除，逐个转移，同样 `O(n)`。

**同模式。** LC 300 最长递增子序列、LC 334 递增的三元子序列、LC 1671 得到山形数组的最少删除次数
