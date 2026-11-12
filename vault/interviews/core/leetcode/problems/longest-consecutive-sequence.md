---
slug: longest-consecutive-sequence
---
## Q
**LC 128 最长连续序列**｜Medium

未排序整数数组 `nums`，求数值连续的最长序列长度（元素不要求相邻），要求 `O(n)`。

## A
**一句话。** 放进集合，只从序列起点（`x-1` 不在集合）向右数，每个数只被数一次。

```python
def longest_consecutive(nums):
    seen = set(nums)
    best = 0
    for x in seen:
        if x - 1 in seen:        # 不是起点，让起点去数
            continue
        end = x + 1
        while end in seen:
            end += 1
        best = max(best, end - x)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 去掉起点检查：每个数都往右数，`range(1000)` 要 `n²/2` 步，超时。
- 遍历 `nums` 而不是 `set`：重复的起点会重复数。
- 改用排序：`O(n log n)` 不达标，且 `[1,0,1,2]` 不去重会得 `2`，应为 `3`。

**追问。**
- 要返回这个序列本身？：记录最优起点和长度，最后 `range(start, start+best)`。
- 数据是流式插入？：用端点长度表，插入 `x` 时合并左右邻居，或用并查集。

**同模式。** LC 674 最长连续递增序列、LC 298 二叉树最长连续序列、LC 947 移除最多的同行或同列石头
