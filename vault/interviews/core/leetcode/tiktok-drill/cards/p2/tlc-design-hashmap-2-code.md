---
id: tlc-design-hashmap-2-code
node: p2.design-hashmap
type: qa
step: 2
---
## Q
**LC 706 设计哈希映射**｜写出 Python 实现

不使用内建哈希表（如 `dict`）实现 `MyHashMap`：`put(key, value)` 插入或更新，`get(key)` 返回值或 `-1`，`remove(key)` 删除。`0 <= key, value <= 10^6`，最多 `10^4` 次调用。

## A
**思路。** 开 `1009`（质数）个桶，每个桶是一个 `[key, value]` 小列表组成的列表。用 `hash(key) % 1009` 定位桶，`put` 在桶里找到相同键就原地更新、找不到就追加；`get` 在桶里找；`remove` 找到后与桶尾交换再弹出。

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

**复杂度。** 每桶平均 `n / 1009` 个元素：三个操作均摊 `O(1 + n/1009)`，`n <= 10^4` 时约 `O(10)`；空间 `O(1009 + n)`。

**写法要点。** `[[] for _ in range(SIZE)]` 每个桶是独立的列表；`_bucket` 抽出「定位桶」，三个方法共用；`for k, v in bucket` 直接解包 `[key, value]`；`pair[1] = value` 修改的是桶里的同一个列表对象，所以是原地更新；`enumerate` 拿到下标后用「与最后一个交换再 `pop()`」代替 `del bucket[i]` 的 `O(len)` 搬移；类属性 `SIZE` 让桶数一处可调；`hash(key)` 对整数就是它自身，写 `hash` 是为了将来键换成字符串等类型时不用改。
