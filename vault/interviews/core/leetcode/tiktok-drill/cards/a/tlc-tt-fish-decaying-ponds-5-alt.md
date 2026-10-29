---
id: tlc-tt-fish-decaying-ponds-5-alt
node: a.tt-fish-decaying-ponds
type: qa
step: 5
---
## Q
**鱼塘捕鱼（产量递减）**｜另一种解法

不用二分，直接模拟“每次捕当前产量最大的鱼塘”，怎么写？它在 `t` 多大时可以接受，什么时候必须用阈值二分？

## A
**思路：最大堆模拟。** 堆里放每个鱼塘的“当前产量”。每个时间单位弹出最大的一个，累加到答案，减去它的 `decay`，仍为正就放回。`heapq` 是最小堆，所以存负数。

```python
import heapq


def max_fish_heap(fish: list[int], decay: list[int], t: int) -> int:
    heap = [(-f, d) for f, d in zip(fish, decay) if f > 0]
    heapq.heapify(heap)                              # O(n) 建堆
    total = 0
    for _ in range(t):
        if not heap:
            break                                    # 所有塘都捞空了
        neg, d = heapq.heappop(heap)
        total += -neg
        if -neg - d > 0:
            heapq.heappush(heap, (neg + d, d))       # 负数加 d 等于产量减 d
    return total
```

运行：`[10, 6]`、`[4, 1]`、`t = 3` → `22`；`[5]`、`[5]`、`t = 4` → `5`；`[3, 3]`、`[1, 1]`、`t = 100` → `12`；`[7]`、`[0]`、`t = 5` → `35`。

**复杂度。** 时间 `O(n + t log n)`，空间 `O(n)`。

**什么时候用哪个。**
- `t` 不大（约 `10^6` 以内）：堆模拟最直观，不容易写错，也很容易改成带约束的版本；先写它作为基线，再说明规模问题。
- `t` 到 `10^9`：堆要循环 `10^9` 次，必须用阈值二分，`O(n log n + n log max(fish))` 与 `t` 无关。
- `decay = 0` 的塘在堆里会一直被放回，没有问题，只是 `t` 大时更慢；二分里要单独记为无限机会。
