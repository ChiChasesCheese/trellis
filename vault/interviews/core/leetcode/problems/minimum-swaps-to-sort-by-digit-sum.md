---
slug: minimum-swaps-to-sort-by-digit-sum
---
## Q
**LC 3551 数位和排序需要的最小交换次数**｜Medium

互不相同的正整数数组 `nums`，按数位和升序（相等时按值升序）排序，求所需的最少交换次数。

## A
**一句话。** 目标顺序唯一，把位置连成置换，每个长度 `L` 的环要 `L - 1` 次交换，总数为 `n - 环数`。

```python
def min_swaps(nums):
    n = len(nums)
    def key(i):
        return sum(map(int, str(nums[i]))), nums[i]
    target = sorted(range(n), key=key)   # 第 j 位放原下标
    seen = [False] * n
    cycles = 0
    for s in range(n):
        if seen[s]:
            continue
        cycles += 1                  # 固定点也是长度 1 的环
        i = s
        while not seen[i]:
            seen[i] = True
            i = target[i]
    return n - cycles
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 排序键漏掉「数位和相等取较小值」：`[18,43,34,16]` 目标错成 `[43,34,16,18]`，得 `3`，应为 `2`。
- 把错位元素个数当答案：`[18,43,34,16]` 四个位置全错，得 `4`，应为 `2`。
- 环数只数长度大于 `1` 的环：固定点也要算，`[22,14,33,7]` 应为 `0`。

**追问。**
- 为什么要求元素互不相同？：否则目标位置不唯一，要在多种匹配里取环数最多的。
- 为什么每个环恰好 `L - 1` 次？：每次交换最多把一个元素放到位，最后一次同时放好两个。

**同模式。** LC 2471 逐层排序二叉树所需的最少操作数、LC 765 情侣牵手、LC 2459 通过移动项目到空白区域来排序数组
