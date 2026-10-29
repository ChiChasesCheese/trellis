---
id: uth-compose-indexed-heap-3-invariants-code
node: compose.indexed-heap
type: qa
step: 3
---
## Q
**不变量与最小实现**｜Java ScheduledThreadPoolExecutor · JDK 21

两个结构要始终一致。写一个带下标的最小堆，说清每个操作先改谁、后改谁。

## A
**不变量。**

- 堆序：每个父节点都不比孩子大。
- 下标表：`pos[key] == i` 当且仅当 `a[i]` 的 key 是 `key`；两个结构的元素个数始终相等。

**顺序。** 数组只通过 `_swap` 改：同一个函数里先换数组的两格，再写两个 `pos`，两个结构在任何一次调用之间都是一致的。删除：先换到末尾，再同时从数组和 `pos` 里去掉，最后才修复堆序。

```python
class IndexedHeap:
    def __init__(self) -> None:
        self.a: list[tuple[int, str]] = []                   # 堆数组：(优先级, key)，小的在上
        self.pos: dict[str, int] = {}                        # key -> 它在 a 里的下标

    def _swap(self, i: int, j: int) -> None:                 # 动数组的唯一入口：交换时同步两个下标
        self.a[i], self.a[j] = self.a[j], self.a[i]
        self.pos[self.a[i][1]], self.pos[self.a[j][1]] = i, j

    def _fix(self, i: int) -> None:                          # 把 i 处的元素放回正确位置：先试上浮，再试下沉
        while i and self.a[i] < self.a[p := (i - 1) // 2]:
            self._swap(i, p)
            i = p
        while (c := 2 * i + 1) < len(self.a):
            if c + 1 < len(self.a) and self.a[c + 1] < self.a[c]:
                c += 1                                       # 取较小的孩子
            if not self.a[c] < self.a[i]:
                break
            self._swap(i, c)
            i = c

    def push(self, key: str, pri: int) -> None:              # 新增，或改已有 key 的优先级
        i = self.pos.setdefault(key, len(self.a))
        self.a[i:i + 1] = [(pri, key)]                       # 新 key 时 i 正好在末尾，等价于 append
        self._fix(i)

    def remove(self, key: str) -> None:
        i = self.pos[key]
        self._swap(i, len(self.a) - 1)                       # 先换到末尾，数组才能保持连续
        del self.pos[self.a.pop()[1]]
        if i < len(self.a):                                  # 换过来的元素可能要上浮，也可能要下沉
            self._fix(i)

    def pop(self) -> str:                                    # 取出最小的 key
        self.remove(key := self.a[0][1])
        return key
```

**坑。** 任何一处交换漏了更新 `pos`，之后的取消就会改错元素。优先级相同时，这里按 key 字典序；JDK 另给每个任务一个递增的 `sequenceNumber`，保证先进先出。

**对应 LeetCode：** 无直接对应的题
