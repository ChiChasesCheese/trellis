---
id: tlc-top-k-frequent-words-4-followup
node: b.top-k-frequent-words
type: qa
step: 4
---
## Q
**LC 692 前K个高频单词**｜追问

面试官接着问：（1）做到 `O(n log k)`，而且要求你手写堆、不能用 `nsmallest`？（2）能不能做到线性时间？（3）单词量是几十亿、一台机器装不下时怎么办？

## A
1. **手写大小为 `k` 的堆**：堆顶是当前 `k` 个里最差的（次数少、平局字典序大），超过 `k` 就弹出；最后从好到差排出来。

```python
import heapq
from collections import Counter


class Entry:
    def __init__(self, freq: int, word: str) -> None:
        self.freq, self.word = freq, word

    def __lt__(self, other: "Entry") -> bool:      # 「更小」= 更差：次数少，或平局时字典序大
        if self.freq != other.freq:
            return self.freq < other.freq
        return self.word > other.word


def top_k_heap(words: list[str], k: int) -> list[str]:
    heap: list[Entry] = []
    for w, c in Counter(words).items():
        heapq.heappush(heap, Entry(c, w))
        if len(heap) > k:
            heapq.heappop(heap)                    # 弹掉最差的
    heap.sort(reverse=True)                        # 最好的在前
    return [e.word for e in heap]
```

运行：样例 1 → `['i', 'love']`，`["a","b","c"], k = 2` → `['a', 'b']`。时间 `O(m log k)`，堆空间 `O(k)`。

2. **线性（桶排序）**：次数在 `1..n` 之间，`buckets[c]` 放次数为 `c` 的单词，从 `n` 往下取，桶内排序后依次加入直到够 `k` 个。计数和扫桶是 `O(n)`，桶内排序只发生在取到的那几个桶上。
3. **分布式**：按 `hash(word) % P` 分片，同一个单词必然落在同一片，每片独立计数并求局部 Top-K，再把 `P` 份 Top-K 合并（`heapq.merge` 或再取一次 Top-K）。只要近似结果时，用 Count-Min Sketch 计数加一个大小为 `k` 的堆，内存与单词种类数无关。

**Python 提醒**：`heapq` 只支持最小堆，元素比较走 `__lt__`；元组里放字符串时无法用取负的技巧反转字典序，必须自定义类或用 `nsmallest(key=...)`。
