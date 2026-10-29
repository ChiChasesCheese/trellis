---
id: tlc-tt-most-frequent-ties-smaller-4-followup
node: a.tt-most-frequent-ties-smaller
type: qa
step: 4
---
## Q
**出现次数最多的元素（并列取较小的）**｜追问

数组版写完后，面试官接着问：（1）数据是流，每来一个数都要能随时回答「出现最多、并列取最小」的元素，怎么做？（2）还要支持删除一个数呢？

## A
1. **只增不删。** 次数只会上涨，答案只会被新来的数「挑战」。维护 `count` 和当前答案 `best`：新来 `x` 后，若 `(count[x], -x) > (count[best], -best)` 就令 `best = x`。每次 `O(1)`。
2. **支持删除。** 次数会下降，原来的答案可能要「退位」，而谁接任无法用一个变量知道。用**懒删除堆**（lazy deletion heap）：每当某个值的次数变化，就把 `(-新次数, 值)` 推进堆；旧条目不删。查询时看堆顶，若它记录的次数和 `count` 里的当前次数不一致，就是过期条目，弹掉继续看。每个值的当前状态都有一个有效条目在堆里，所以第一个有效的堆顶就是答案。

```python
import heapq
from collections import Counter


class StreamMode:
    def __init__(self) -> None:
        self.count: Counter[int] = Counter()
        self.heap: list[tuple[int, int]] = []          # (-次数, 数值)，可能含过期条目

    def add(self, x: int) -> None:
        self.count[x] += 1
        heapq.heappush(self.heap, (-self.count[x], x))

    def remove(self, x: int) -> None:
        if self.count[x] == 0:
            return
        self.count[x] -= 1
        if self.count[x]:
            heapq.heappush(self.heap, (-self.count[x], x))
        else:
            del self.count[x]

    def mode(self) -> int | None:
        while self.heap:
            neg, x = self.heap[0]
            if self.count.get(x, 0) == -neg:           # 与当前计数一致才有效
                return x
            heapq.heappop(self.heap)                    # 过期条目，弹掉
        return None
```

   运行：依次 `add` `3,1,3,1,2` 后 `mode()` → `1`；`remove(1)` 后 → `3`；再 `remove(3)` 两次 → `1`。每次操作均摊 `O(log m)`，`m` 为推入堆的条目数。要严格 `O(1)` 可以用「次数 → 值集合」的桶加最大次数指针（LC 895、LC 432 的思路），但桶内取最小值还需要有序结构。

**Python 提醒**：`Counter` 访问不存在的键返回 `0` 但**不会**插入它，而 `count[x] -= 1` 会插入；次数归零时要 `del`，否则 `len(count)` 和遍历里会留着 0 次的键。
