---
id: tlc-shortest-subarray-with-sum-at-least-k-5-alt
node: a.shortest-subarray-with-sum-at-least-k
type: qa
step: 5
---
## Q
**LC 862 和至少为 K 的最短子数组**｜另一种解法

如果想不起来单调队列，有没有更容易写对的 `O(n log n)` 解法？它和暴力枚举各适合什么场合？

## A
**思路。** 用最小堆（`heapq`）代替单调队列。堆里放 `(前缀和, 下标)`；对每个 `j`，只要堆顶的前缀和满足 `cur - 堆顶前缀和 >= k`，就弹出并更新答案（弹出的起点之后只会更长，和队首弹出同理）。不需要手工维护单调性，堆自动让「前缀和最小的起点」在最上面。

```python
from heapq import heappop, heappush
from itertools import accumulate


def shortest_subarray_heap(nums: list[int], k: int) -> int:
    pre = [0, *accumulate(nums)]
    heap: list[tuple[int, int]] = []       # (前缀和, 下标)，堆顶前缀和最小
    best = len(nums) + 1
    for j, cur in enumerate(pre):
        while heap and cur - heap[0][0] >= k:
            best = min(best, j - heappop(heap)[1])
        heappush(heap, (cur, j))
    return best if best <= len(nums) else -1
```

运行：`[1]`、`k = 1` → `1`；`[1,2]`、`k = 4` → `-1`；`[2,-1,2]`、`k = 3` → `3`；`[84,-37,32,40,95]`、`k = 167` → `3`。

**为什么对。** 每个起点只在「第一次被某个 `j` 配对成功」时被弹出，而此时的 `j` 就是它能得到的最短右端（更大的 `j` 只会更长）。堆顶是前缀和最小的候选，若堆顶都不满足，其余起点更不可能满足。

**取舍。** 堆版每个下标入堆出堆一次，`O(n log n)`，不用推导队尾淘汰，写错的概率小；单调队列版 `O(n)`，面试里是预期的最优解。暴力枚举所有 `(i, j)` 加前缀和是 `O(n^2)`，`n` 到几百时可以当对照写，`n = 10^5` 会超时。先说出暴力和前缀和，再给单调队列，被追问不会写时退到堆版也是正确的。
