---
slug: tt-idempotent-versioned-update
---
## Q
**幂等、带版本号的数据更新**｜Medium

实现 `VersionedStore`：`update(request_id, key, value, expected_version)` 仅当 `key` 当前版本等于 `expected_version` 时写入并版本加 1，返回 `(True, 新版本)`，否则返回 `(False, 当前版本)`；同一 `request_id` 重试要原样返回第一次的结果；`get(key)` 返回 `(value, version)`，不存在为 `(None, 0)`。

## A
**一句话。** 版本号做乐观并发控制（CAS）挡住旧数据的写，`request_id → 第一次结果` 表做幂等，成功和冲突的结果都要记。

```python
class VersionedStore:
    def __init__(self):
        self.data = {}      # key -> (value, version)
        self.done = {}      # request_id -> 第一次的结果

    def get(self, key):
        return self.data.get(key, (None, 0))

    def update(self, rid, key, value, expected):
        if (prev := self.done.get(rid)) is not None:
            return prev     # 重试：原样返回，不再写
        _, version = self.get(key)
        if version == expected:          # compare-and-set
            self.data[key] = (value, version + 1)
            result = (True, version + 1)
        else:
            result = (False, version)
        self.done[rid] = result          # 冲突结果也记
        return result
```

**复杂度。** 时间 每次操作 `O(1)`，空间 `O(key 数 + request_id 数)`。

**易错点。**
- 没有幂等表：`update("r1","a","x",0)` 成功后重试得 `(False, 1)`，应为 `(True, 1)`。
- 只缓存成功结果：冲突过的请求带同一 `request_id` 重试可能真的写入，同一请求出现两种结果。
- 冲突时返回 `expected` 而不是当前版本：客户端还得再 `get` 一次。

**追问。**
- `request_id` 表无限增长？：只保留重试窗口内的记录，从最旧一端淘汰；过期后的重试由 CAS 兜底，只会冲突不会重复写。
- 多线程？：「查幂等表、CAS、记结果」必须在同一把锁里，可按 key 分段加锁。

**同模式。** LC 981 基于时间的键值存储、LC 146 LRU 缓存、LC 1146 快照数组、LC 2502 设计内存分配器
