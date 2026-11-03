---
id: craft-sentinels-5-scales-tombstone
node: craft.idioms.sentinels
type: qa
step: 5
---
## Q
**哨兵 · 从堆里的墓碑到 Kafka 压缩主题的删除标记**｜写法

带过期时间的缓存用小根堆按过期时间出堆。删除一个键时，不能从堆中间拿掉元素（要 O(n)），怎么办？分布式日志（如 Kafka 的压缩主题）里「删除一个键」又是怎么做的？它们共用的想法是什么？

## A
**要点。** 都是墓碑（tombstone）：不动已有结构，只写一个「这条已经没用」的标记，真正的清除推迟到读到它或批量整理时。堆里把条目的键换成哨兵，弹出时遇到就丢弃；追加式日志里写一条值为 `None` 的记录，压缩（compaction）时每个键只保留最后一条，最后一条是墓碑就整个键删掉。

```python
import heapq

_REMOVED = object()                       # 堆里的墓碑

class TTLHeap:
    """按过期时间出堆；删除不动堆，只给条目打墓碑。"""
    def __init__(self) -> None:
        self.heap: list[list] = []
        self.entry: dict[str, list] = {}
    def put(self, key: str, exp: float) -> None:
        self.delete(key)
        e = [exp, key]
        self.entry[key] = e
        heapq.heappush(self.heap, e)
    def delete(self, key: str) -> None:
        e = self.entry.pop(key, None)
        if e is not None:
            e[1] = _REMOVED               # O(1)：堆里的位置不能乱动
    def pop_expired(self, now: float) -> list[str]:
        out = []
        while self.heap and self.heap[0][0] <= now:
            exp, key = heapq.heappop(self.heap)
            if key is not _REMOVED:       # 墓碑直接丢掉
                out.append(key); del self.entry[key]
        return out

h = TTLHeap()
h.put("a", 1); h.put("b", 2); h.put("c", 3)
h.delete("b")
print(len(h.heap), h.pop_expired(5), len(h.heap))

log = [("u1", "alice"), ("u2", "bob"), ("u1", "alice2"), ("u2", None)]   # 最后一条：删除 u2
def compact(log):
    latest = {}
    for k, v in log:
        latest[k] = v                      # 每个 key 只留最后一条
    return [(k, v) for k, v in latest.items() if v is not None]
print(compact(log))
```

实际输出：

```
3 ['a', 'c'] 0
[('u1', 'alice2')]
```

**为什么。** 第一行说明：删除后堆仍有 3 个元素，弹出过期项时墓碑被顺手清走，`b` 没有出现在结果里。两处的代价相同：墓碑占着空间，直到被清除；墓碑太多时要主动压实（重建堆、触发压缩）。

**变化。** 堆里的墓碑是进程内的 `object()`，用 `is` 判断；日志里的墓碑要跨进程、跨语言，所以只能是数据：一个约定的空值。这也意味着在这种系统里，「值为空」不能再同时是合法业务值，和第一张卡片是同一个问题的另一面。Kafka 里墓碑还要保留一段时间再清除，让落后的消费者也能看到这次删除。
