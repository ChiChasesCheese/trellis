---
id: tlc-design-hashmap-4-followup
node: a.design-hashmap
type: qa
step: 4
---
## Q
**LC 706 设计哈希映射**｜追问

面试官接着问：（1）键越来越多，桶数固定会变慢，怎么办？（2）如果不用拉链法，改用开放寻址？（3）多线程同时读写怎么保证安全？

## A
1. **动态扩容**：记录元素个数 `size`，当装载因子 `size / 桶数` 超过 `0.75` 时，把桶数翻倍并把所有键值对重新散列到新桶数组里。单次扩容 `O(n)`，但每次翻倍后要再插入 `O(桶数)` 个元素才会触发下一次，所以均摊 `O(1)`。
```python
class ResizableMap:
    def __init__(self) -> None:
        self.size = 0
        self.buckets: list[list[list[int]]] = [[] for _ in range(8)]

    def _grow(self) -> None:
        old = self.buckets
        self.buckets = [[] for _ in range(len(old) * 2)]
        for bucket in old:
            for key, value in bucket:
                self.buckets[hash(key) % len(self.buckets)].append([key, value])

    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[hash(key) % len(self.buckets)]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self.size += 1
        if self.size > 0.75 * len(self.buckets):      # 装载因子超过 0.75：桶数翻倍，全部重新散列
            self._grow()
```
   `get` 和 `remove` 同基础版，只是桶数改用 `len(self.buckets)`，`remove` 成功时 `size -= 1`。
2. **开放寻址**（open addressing）：所有键值对放在一个数组里，冲突时按线性探测（`i, i+1, i+2, ...`）找下一个空槽。删除不能直接清空槽，否则探测链断开，后面的键会找不到；要放一个「墓碑」标记（tombstone），`get` 遇到墓碑继续探测，`put` 可以复用墓碑。装载因子必须明显小于 1（常取 0.5 左右）。
3. **并发**：最简单是一把全局锁；更好的是分段锁（lock striping）——把桶分成若干段，每段一把锁，不同段的操作并行；读多写少时用读写锁，或像 Java 的 `ConcurrentHashMap` 那样对桶头做 CAS。

**Python 提醒**：`hash(key)` 对整数就是它本身（`-1` 的哈希是 `-2`），对字符串每次解释器启动会随机加盐（`PYTHONHASHSEED`），所以不要把 `hash(str)` 的结果持久化到磁盘或跨进程使用。取模 `hash(key) % n` 在 Python 里对负数也返回非负数，不会出现 C 语言里负下标的问题。
