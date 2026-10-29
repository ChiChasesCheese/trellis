---
id: uth-python-dict-3-collision
node: python.dict
type: qa
step: 3
---
## Q
**哈希全冲突时 dict 会怎样**｜Python · CPython 3.14

自定义类的 `__hash__` 总返回 1，往 `dict` 里插入 500、1000、2000 个这样的 key，耗时怎么变？

## A
**背景。** `dict` 的 O(1) 建立在一个前提上：不同的 key 大多落在不同的槽。如果所有 key 的哈希值都相同，第 n 个 key 要先跳过前面 n−1 个被占的槽才找到空位，哈希表就退化成了一条链。

**结构。** 所有 key 争同一条探测序列，每次插入都要先走过前面已占的槽。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<line x1="40" y1="170" x2="320" y2="170" stroke-width="1.2" stroke="currentColor"/>
<line x1="40" y1="170" x2="40" y2="24" stroke-width="1.2" stroke="currentColor"/>
<rect x="70" y="162.063" width="48" height="7.93651" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="94" y="156.063" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2.8 ms</text>
<text x="94" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">500</text>
<rect x="150" y="139.104" width="48" height="30.8957" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="174" y="133.104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10.9 ms</text>
<text x="174" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1000</text>
<rect x="230" y="45" width="48" height="125" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">44.1 ms</text>
<text x="254" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2000</text>
<text x="60" y="50" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数量 x2</text>
<text x="60" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">耗时 x4</text>
<text x="40" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">__hash__ 恒为 1 插入 n 个 key</text>
</svg>
```

**细节。**

- 单次插入退化为 O(n)，n 次就是 O(n²)。
- 本机实测：2.8、10.9、44.1 毫秒，数量翻倍，耗时约 4 倍。

**为什么。** O(1) 全靠哈希分布均匀，所以 Python 对外部输入的字符串哈希加了随机化来防攻击（攻击者故意构造一批哈希相同的输入）。

**坑。** 自定义 `__hash__` 必须与 `__eq__` 一致，并混合所有参与比较的字段。

**例题：** LC 706 设计哈希映射

不用内建哈希表，设计 `MyHashMap`：`put(key, value)` 已存在则更新；`get(key)` 不存在返回 `-1`；`remove(key)` 删除映射。`0 <= key, value <= 10^6`，最多调用 `10^4` 次。

```python
class MyHashMap:
    SIZE = 1009                               # 质数个桶：key 有规律时也分得开

    def __init__(self) -> None:
        self.buckets: list[list[list[int]]] = [[] for _ in range(self.SIZE)]   # 每个桶是一条链：[[key, value], ...]

    def _bucket(self, key: int) -> list[list[int]]:
        return self.buckets[hash(key) % self.SIZE]

    def put(self, key: int, value: int) -> None:
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:                # 已存在：原地更新，不能再追加一条
                pair[1] = value
                return
        bucket.append([key, value])

    def get(self, key: int) -> int:
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = bucket[-1]        # 链内顺序无所谓：和最后一个交换再弹出，O(1) 删除
                bucket.pop()
                return
```
