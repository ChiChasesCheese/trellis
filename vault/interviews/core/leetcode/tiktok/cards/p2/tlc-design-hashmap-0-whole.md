---
id: tlc-design-hashmap-0-whole
node: p2.design-hashmap
type: qa
---
## Q
**LC 706 设计哈希映射**｜Easy · LC TikTok 近 6 个月热度 50/100（全时段 62） · 近一年被问：美国 2 次、国内 1 次 · CodeTop 国内累计 3 次 · 最近 2026-08-13（国内面试记录）

不使用任何内建的哈希表库设计一个哈希映射（HashMap）。实现 `MyHashMap` 类：`MyHashMap()` 初始化空映射；`void put(int key, int value)` 插入键值对，若 `key` 已存在则更新其值；`int get(int key)` 返回 `key` 对应的 `value`，不存在返回 `-1`；`void remove(key)` 若存在 `key` 的映射则移除它。`0 <= key, value <= 10^6`，最多调用 `10^4` 次 `put`、`get` 和 `remove`。例：依次 `put(1,1)`、`put(2,2)`、`get(1)`、`get(3)`、`put(2,1)`、`get(2)`、`remove(2)`、`get(2)` 返回 `1, -1, 1, -1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 拉链法（separate chaining）：开一个固定个数（质数）的桶数组，`key % 桶数` 决定放进哪个桶，桶里是 `[key, value]` 的小列表；`put` / `get` / `remove` 都只扫自己那个桶。均摊 `O(1)`。

**识别。** 「自己实现哈希表」就是考哈希函数、冲突处理、增删改查四件事。冲突不可避免（`10^6` 个可能的键，桶数远少于此），拉链法最容易写对。键范围只有 `0..10^6`，也可以用大小 `10^6 + 1` 的数组直接寻址，那是特例；面试要展示的是通用的哈希表设计。

**推导。** 暴力：用一个 `[key, value]` 列表存所有键值对，每次线性扫描，`O(n)` → 浪费：每次都扫全部 → 用哈希函数把键映射到一个桶，只扫桶里的少数元素 → 桶数取质数（`1009`）。

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

运行：依次 `put(1,1)`、`put(2,2)`、`get(1)`、`get(3)`、`put(2,1)`、`get(2)`、`remove(2)`、`get(2)` 的返回值是 `[None, None, 1, -1, None, 1, None, -1]`。

**复杂度。** 平均每个桶 `n / 1009` 个元素：`put` / `get` / `remove` 均摊 `O(1 + n/B)`（`B = 1009`）；`n <= 10^4` 时每个桶平均不到 `10` 个。空间 `O(B + n)`。

**拓展优化。**
- 动态扩容：装载因子（元素数 / 桶数）超过 `0.75` 就把桶数翻倍并全部重新散列（rehash），一次 `O(n)` 但每翻倍才发生一次，均摊 `O(1)`。

```python
class MyHashMap:
    def __init__(self) -> None:
        self.size = 8                              # 初始桶数小，靠扩容跟上元素数
        self.count = 0
        self.buckets: list[list[list[int]]] = [[] for _ in range(self.size)]

    def _resize(self) -> None:
        old = self.buckets
        self.size *= 2                             # 桶数翻倍：每个桶的平均长度减半
        self.buckets = [[] for _ in range(self.size)]
        for bucket in old:
            for pair in bucket:                    # 桶数变了，key % size 也变，必须全部重放
                self.buckets[pair[0] % self.size].append(pair)

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[key % self.size]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self.count += 1
        if self.count > 0.75 * self.size:          # 装载因子超标：扩容保证链长均摊 O(1)
            self._resize()

    def get(self, key: int) -> int:
        for k, v in self.buckets[key % self.size]:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self.buckets[key % self.size]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = bucket[-1]             # 和最后一个交换再弹出：链内顺序无所谓
                bucket.pop()
                self.count -= 1
                return
```

**易错点。**
- `put` 遇到已存在的键必须更新而不是追加：不去重时，`put(2,2)`、`put(2,1)` 后 `get(2)` 返回 `2`（找到第一条旧记录），正确是 `1`；再 `remove(2)` 只删掉一条，`get(2)` 返回 `1` 而不是 `-1`。
- 桶数组不能写成 `[[]] * SIZE`：所有桶会是同一个列表对象，`b[0].append(1)` 之后 `[[1], [1], [1]]`，所有键混在一起。
- `get` 找不到返回 `-1`，不能抛异常；`remove` 对不存在的键什么都不做。

**追问。**
- 开放寻址（open addressing）：冲突时往后探测，删除要用墓碑标记，否则会截断探测链。
- 并发安全：加一把全局锁，或分段锁（lock striping，每段桶一把锁）。

**同模式。** LC 705 设计哈希集合、LC 146 LRU 缓存、LC 380 O(1) 时间插入、删除和获取随机元素、LC 460 LFU 缓存。
