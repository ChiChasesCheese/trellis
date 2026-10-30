---
id: tlc-find-the-duplicate-number-4-followup
node: p4.find-the-duplicate-number
type: qa
step: 4
---
## Q
**LC 287 寻找重复数**｜追问

面试官接着问：（1）怎么证明一定存在重复数？（2）不用快慢指针，还有 `O(1)` 空间、不改数组的办法吗？（3）如果允许修改数组呢？（4）有多个重复数，或者要找所有缺失的数呢？

## A
1. **存在性**：`n + 1` 个数放进 `n` 个可能的值，鸽巢原理，至少有一个值出现两次。
2. **按值二分**：答案在 `[1, n]`；对 `mid`，数数组里 `<= mid` 的元素个数。若个数超过 `mid`，由鸽巢原理 `[1, mid]` 里有重复数，否则重复数在 `(mid, n]`。每轮 `O(n)`，共 `log n` 轮，`O(n log n)` 时间、`O(1)` 空间、不改数组。

```python
def find_duplicate_bisect(nums: list[int]) -> int:
    lo, hi = 1, len(nums) - 1              # 答案在 [1, n]
    while lo < hi:
        mid = (lo + hi) // 2
        count = sum(1 for x in nums if x <= mid)   # 值不超过 mid 的元素个数
        if count > mid:                    # 鸽巢原理：[1, mid] 里至少有重复的数
            hi = mid
        else:
            lo = mid + 1
    return lo
```

`[1,3,4,2,2]` → `2`，`[3,3,3,3,3]` → `3`；`n = 10^5` 约 `0.02` 秒。
3. **允许修改**：循环交换，把每个值 `x` 放到下标 `x` 处（下标 `0` 留作空位），放不下（目标位置已经是同一个值）就是重复数；或者遍历时把 `nums[abs(x)]` 取负，碰到已经为负的就是重复数。都是 `O(n)` 时间，但破坏了数组。
4. **推广**：重复数不止一个且每个出现两次（LC 442）、找所有消失的数（LC 448），都靠"值当下标 + 原地标记"；Floyd 只能处理"恰好一个重复值"的情形，因为环只有一个入口。

**Python 提醒**：`sum(1 for x in nums if x <= mid)` 用生成器逐个计数，不创建中间列表。Python 没有 do-while，`while True: … if cond: break` 是惯用写法。
