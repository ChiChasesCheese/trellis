---
id: tlc-tt-idempotent-versioned-update-2-code
node: p4.tt-idempotent-versioned-update
type: qa
step: 2
---
## Q
**幂等、带版本号的数据更新**｜写出 Python 实现

实现 `VersionedStore`：`update(request_id, key, value, expected_version)` 在版本相等时写入并把版本加 1，返回 `(True, 新版本)`，否则返回 `(False, 当前版本)`；同一 `request_id` 重试原样返回第一次的结果；`get(key)` 返回 `(value, version)`，不存在为 `(None, 0)`。调用总数 `<= 10^5`。

## A
**思路。** 两个字典：`data` 存 `key → (value, version)`，`done` 存 `request_id → 第一次结果`。`update` 先查 `done`，命中就原样返回；否则做比较并更新，把结果（成功或冲突）记进 `done`。

```python
class VersionedStore:
    def __init__(self) -> None:
        self.data: dict[str, tuple[str, int]] = {}           # key -> (value, version)
        self.done: dict[str, tuple[bool, int]] = {}          # request_id -> 第一次的结果

    def get(self, key: str) -> tuple[str | None, int]:
        return self.data.get(key, (None, 0))                 # 不存在的 key 版本为 0

    def update(self, request_id: str, key: str, value: str, expected_version: int) -> tuple[bool, int]:
        """返回 (是否写入, 版本)：成功时是新版本，冲突时是当前版本。"""
        if (prev := self.done.get(request_id)) is not None:
            return prev                                      # 重试：原样返回，不再写
        _, version = self.get(key)
        if version == expected_version:                      # 比较并更新（compare-and-set）
            self.data[key] = (value, version + 1)
            result = (True, version + 1)
        else:
            result = (False, version)
        self.done[request_id] = result                       # 冲突结果也要记住
        return result
```

运行：`update("r1","a","x",0)` → `(True, 1)`；重试同一调用 → `(True, 1)`；`update("r2","a","y",0)` → `(False, 1)`；`update("r3","a","y",1)` → `(True, 2)`；`get("a")` → `('y', 2)`，`get("b")` → `(None, 0)`；再 `update("r2","a","y",2)` → `(False, 1)`。

**复杂度。** 每次操作 `O(1)`；空间 `O(key 数 + request_id 数)`。

**写法要点。** 值和版本存成一个元组，一次读出、一次写入，不会出现值改了版本没改的中间状态；`dict.get(key, (None, 0))` 把「不存在」统一成版本 0，新建 key 不用特判；海象运算符 `(prev := ...)` 把查表和判断合成一行；判断写 `is not None` 而不是真假判断：意图明确，结果类型以后换成可能为假的值（如 `0`）也不会出错。
