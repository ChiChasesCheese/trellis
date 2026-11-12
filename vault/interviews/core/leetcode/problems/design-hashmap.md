---
slug: design-hashmap
---
## Q
**LC 706 设计哈希映射**｜Easy

不用内建哈希表，实现 `MyHashMap` 的 `put(key, value)`（已存在则更新）、`get(key)`（不存在返回 `-1`）、`remove(key)`。

## A
**一句话。** 拉链法：固定个数（质数）的桶，`key % 桶数` 选桶，桶里存 `[key, value]` 小列表，操作只扫自己的桶。

```python
class MyHashMap:
    SIZE = 1009                  # 质数个桶

    def __init__(self):
        self.buckets = [[] for _ in range(self.SIZE)]

    def _bucket(self, key):
        return self.buckets[key % self.SIZE]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:   # 已存在：原地更新
                pair[1] = value
                return
        bucket.append([key, value])

    def get(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = bucket[-1]   # 换到末尾再弹，O(1)
                bucket.pop()
                return
```

**复杂度。** 时间均摊 `O(1 + n/B)`（`B` 为桶数），空间 `O(B + n)`。

**易错点。**
- `put` 遇到已有键只追加：`put(2,2)`、`put(2,1)` 后 `get(2)` 返回 `2`，应为 `1`。
- 桶数组写成 `[[]] * SIZE`：所有桶是同一个列表，键全混在一起。

**追问。**
- 开放寻址怎么删除？：用墓碑标记，否则会截断探测链。
- 要并发安全？：全局锁，或分段锁（每段桶一把锁）。

**同模式。** LC 705 设计哈希集合、LC 146 LRU 缓存、LC 380 O(1) 时间插入、删除和获取随机元素、LC 460 LFU 缓存
