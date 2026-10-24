---
id: tlc-patterns-design-4-hashmap
node: patterns.design
type: qa
step: 4
---
## Q
**数据结构设计题｜不用内置字典设计哈希映射（LC 706）**

哈希映射的三个核心部件是什么？冲突怎么处理？桶数量为什么取质数？

## A
三部件：**哈希函数**（把键映射成桶号）、**桶数组**、**冲突处理**（不同键落到同一个桶）。最简单的冲突处理是**链地址法**：每个桶是一个列表，存 `[key, value]`。

```python
class MyHashMap:
    SIZE = 769                             # 质数个桶，减少冲突

    def __init__(self) -> None:
        self.buckets: list[list[list[int]]] = [[] for _ in range(self.SIZE)]

    def _bucket(self, key: int) -> list[list[int]]:
        return self.buckets[key % self.SIZE]

    def put(self, key: int, value: int) -> None:
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value            # 已存在：更新
                return
        bucket.append([key, value])

    def get(self, key: int) -> int:
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                return

m = MyHashMap(); m.put(1, 1); m.put(2, 2)
print(m.get(1), m.get(3))   # 1 -1
m.put(2, 1); print(m.get(2))   # 1
m.remove(2); print(m.get(2))   # -1
```

- 约束 `0 <= key <= 10^6`、最多 `10^4` 次操作：`769` 个桶时每桶平均不到 14 个元素。质数模数让规律性强的键（比如都是 `1000` 的倍数）更均匀。
- 平均 `O(1)`，最坏（全部冲突）`O(n)`。
- 真实实现会在**负载因子**（元素数 / 桶数）超过阈值时**扩容并重新哈希**；面试里可以口述。
- 键范围小（`<= 10^6`）也可直接用长度 `10^6 + 1` 的数组，`O(1)` 且最简单，但占内存。
- 其他冲突处理：开放寻址（线性探测）。删除要用"墓碑"标记，否则会截断探测链。
