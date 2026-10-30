---
id: tlc-tt-kv-store-snapshot-restore-2-code
node: p4.tt-kv-store-snapshot-restore
type: qa
step: 2
---
## Q
**带快照与恢复的内存键值存储**｜写出 Python 实现

写类 `KVStore`：`put(key, value)`、`get(key)`（不存在返回 `None`）、`delete(key)`（成功返回 `True`）、`snapshot() -> str`、`restore(snap)`。key、value 是任意字符串（可为空，可含冒号、换行、中文）；序列化格式自己设计，不用 `json` / `pickle`；`restore` 遇到损坏的数据抛 `ValueError`，且原存储不变。

## A
**思路。** 每个字符串编码成 `长度:内容`，快照 = 条目数 + 依次的 key、value。解码时用 `str.find(":")` 找到长度的结尾，按长度切出内容。`restore` 先解析到临时字典，全部成功、没有多余数据才赋给 `self.data`。

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

运行：`put("a", "1")`、`put("b:c", "x\ny")`、`put("", "")` 后 `snapshot()` → `'1:31:a1:13:b:c3:x\ny0:0:'`；改动、删除、新增之后 `restore`，`data` 回到 `{'a': '1', 'b:c': 'x\ny', '': ''}`，新增的 key `z` 的 `get` 为 `None`；空存储的快照 `'1:0'`；`restore("3:abc")` 抛 `ValueError`，原数据不变；`""`、`"1:1"`、`"1:2"`、`"x"`、`"1:11:a"` 全部被拒绝。

**复杂度。** `snapshot`、`restore` 为 `O(总字符数)`；`put`、`get`、`delete` 为 `O(1)`。

**写法要点。**
- `str.find(":", pos)` 从指定位置查找，返回 `-1` 表示没有；解码是一次指针前进，没有 `split`、没有正则回溯。
- `"".join(parts)`：先收集片段再一次拼接，比反复 `+=` 字符串省复制。
- `dict.pop(key, None) is not None`：一步完成“删除并告诉我是否存在”，但值本身若可能是 `None` 就不适用；这里值是字符串，没有这个问题。
- 内部函数 `_encode_str`、`_read_str` 以下划线开头：编码细节不对外暴露，改格式只动这两处。
