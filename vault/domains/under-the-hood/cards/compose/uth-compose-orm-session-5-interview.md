---
id: uth-compose-orm-session-5-interview
node: compose.orm-session
type: qa
step: 5
---
## Q
**借到面试题上：先记账，再一次提交**｜SQLAlchemy · 2.0.55

面试要你设计带「事务」的内存存储：先改，最后一次生效，出错能回到原样。Session 的骨架怎样借过来？

## A
**背景。** 这是 Session 的缩小版：一份已提交的数据、一份待办、提交时才应用。

**结构。**

- `data`：已提交的内容
- `pending`：事务里的写入，删除用一个特殊标记记下
- `get`：先查 `pending`，再查 `data`
- `commit`：把 `pending` 整体应用到 `data`；`rollback`：丢掉 `pending`

**为什么。** 出错时 `data` 从没被改过，回滚就是丢掉 `pending`，O(1)。下面的 `restore` 用的是同一招：先把快照解析进临时字典 `loaded`，全部成功才 `self.data = loaded`，数据损坏时原存储不变。flush 放在数据库事务里、失败整体回滚，目的也相同。

**例题：** 内存 KV 存储：快照与恢复

实现内存键值存储 `KVStore`：`put`、`get`、`delete`，再加 `snapshot()` 把全部数据序列化成字符串、`restore(data)` 用它恢复到快照时刻的状态。序列化格式自己设计，不能用现成的 `json` 或 `pickle`；key 和 value 可以含冒号、换行等任意字符；传给 `restore` 的数据损坏时要抛 `ValueError`，且原存储保持不变。

```python
def _encode_str(s: str) -> str:
    return f"{len(s)}:{s}"                         # 长度前缀：内容里出现什么字符都不会和格式冲突


def _read_str(data: str, pos: int) -> tuple[str, int]:
    colon = data.find(":", pos)
    if colon == -1 or not data[pos:colon].isdecimal():
        raise ValueError(f"bad length at {pos}")
    end = colon + 1 + int(data[pos:colon])
    if end > len(data):
        raise ValueError("truncated data")
    return data[colon + 1:end], end


class KVStore:
    def __init__(self) -> None:
        self.data: dict[str, str] = {}

    def put(self, key: str, value: str) -> None:
        self.data[key] = value

    def get(self, key: str) -> str | None:
        return self.data.get(key)

    def delete(self, key: str) -> bool:
        return self.data.pop(key, None) is not None

    def snapshot(self) -> str:
        """格式：先写条目数，再依次写 key、value，每个字符串都是 长度:内容。"""
        parts = [_encode_str(str(len(self.data)))]
        for key, value in self.data.items():
            parts.append(_encode_str(key))
            parts.append(_encode_str(value))
        return "".join(parts)

    def restore(self, snap: str) -> None:
        """先解析到临时字典，全部成功才替换：数据损坏时原存储不变。"""
        count_text, pos = _read_str(snap, 0)
        if not count_text.isdecimal():
            raise ValueError("bad count")
        loaded: dict[str, str] = {}
        for _ in range(int(count_text)):
            key, pos = _read_str(snap, pos)
            value, pos = _read_str(snap, pos)
            loaded[key] = value
        if pos != len(snap):
            raise ValueError("trailing data")
        self.data = loaded
```
