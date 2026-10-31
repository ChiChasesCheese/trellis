---
id: tlc-top-k-frequent-elements-2-code
node: p2.top-k-frequent-elements
type: qa
step: 2
---
## Q
**LC 347 前 K 个高频元素**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `10^5`，元素在 `[-10^4, 10^4]`）和整数 `k`（`1` 到不同元素的个数），返回出现频率前 `k` 高的元素，顺序任意，答案唯一。要求时间复杂度优于 `O(n log n)`。

## A
**思路。** `Counter` 统计频次；建 `n + 1` 个桶，下标是频次，把每个元素放进它频次对应的桶；从最高频的桶往低频的桶依次取，凑够 `k` 个就返回。

```python
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]   # 下标 = 出现次数
    for x, c in count.items():
        buckets[c].append(x)
    ans: list[int] = []
    for bucket in reversed(buckets):          # 从高频到低频
        ans.extend(bucket)
        if len(ans) >= k:
            return ans[:k]
    return ans
```

运行：`([1,1,1,2,2,3], 2)` → `[1, 2]`，`([1], 1)` → `[1]`，`([1,2,1,2,1,2,3,1,3,2], 2)` → `[1, 2]`，`([4,4,5,6], 3)` → `[4, 5, 6]`。

**复杂度。** 时间 `O(n)`：`Counter` 一遍、分桶最多 `n` 个元素、倒序扫桶总共 `n + 1` 个桶；空间 `O(n)`。

**写法要点。** `Counter(nums)` 是 C 实现的计数，比手写 `dict.get` 循环快；`[[] for _ in range(...)]` 每个桶是独立的列表，写成 `[[]] * (n+1)` 会让所有桶共享同一个列表；`reversed(buckets)` 不复制列表。不要求线性时，`[x for x, _ in count.most_common(k)]` 一行就够，它内部用 `heapq.nlargest`，`O(n log k)`；`heapq.nlargest(k, count, key=count.get)` 是同样的复杂度。
