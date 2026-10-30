---
id: tlc-tt-kv-store-snapshot-restore-0-whole
node: p4.tt-kv-store-snapshot-restore
type: qa
---
## Q
**带快照与恢复的内存键值存储**｜Medium · 近一年被问：美国 2 次、国内 0 次 · 最近 2026-10-15（面试记录）

实现内存键值存储 `KVStore`：`put(key, value)`、`get(key)`（不存在返回 `None`）、`delete(key)`（删除成功返回 `True`），再加两个操作：`snapshot()` 把当前全部数据**序列化**成一个字符串返回；`restore(data)` 用 `snapshot` 返回的字符串把存储恢复到快照时刻的状态，覆盖当前内容。序列化格式要自己设计，不能调用现成的 `json` / `pickle`。key 和 value 都是字符串，可以是空串，可以包含冒号、分号、换行、引号等任意字符（包括中文和表情符号）；快照之后的写入不能影响已经取出的快照；传给 `restore` 的数据损坏时要抛 `ValueError`，且原存储保持不变。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用「长度前缀」（length-prefix）编码：每个字符串写成 `长度:内容`，先写条目数，再依次写每个 key 和 value；解码时读到冒号前的数字就知道要取多少个字符，内容里出现什么字符都不会和格式冲突。`restore` 先解析到临时字典，全部成功才替换，失败原存储不变。`O(总字符数)`。

**识别。** 「自己写序列化」的难点不在存取，而在**格式能不能无歧义地解回来**：如果用分隔符（逗号、等号、换行）拼接，key 或 value 里一旦含有分隔符，解析就出错。通用的做法有两种：转义（escape）分隔符，或者长度前缀。长度前缀不需要扫描内容、不需要转义，解码是一次线性读取。「快照之后的写入不能污染快照」意味着快照必须是不可变的值（字符串），而不是对内部字典的引用。

**推导。** 暴力：`"k=v;"` 这样拼接，`put("a=b", "c")` 之后快照是 `a=b=c;`，按第一个 `=` 拆开就得到 key `a`、value `b=c`，数据错了。第二步：给分隔符加转义，要同时处理转义符本身，规则容易漏。洞察：先写长度，再写内容，内容按长度整段读取，不再需要判断“这里是不是分隔符”。条目数写在最前面，截断也能被发现。

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

运行：`put("a", "1")`、`put("b:c", "x\ny")`、`put("", "")` 后 `snapshot()` → `'1:31:a1:13:b:c3:x\ny0:0:'`（条目数 `3`，随后是 key `a`、value `1`、key `b:c`、value `x\ny`、两个空串）；再改动 `a`、删除 `b:c`、新增 `z`，`restore` 之后 `data` 回到 `{'a': '1', 'b:c': 'x\ny', '': ''}`，`get("z")` 为 `None`；空存储的快照是 `'1:0'`；`restore("3:abc")`（条目数不是数字）抛 `ValueError`，原数据不变；`""`、`"1:1"`、`"1:2"`、`"x"`、`"1:11:a"`（尾部多余）都被拒绝。

**复杂度。** `snapshot` 与 `restore` 都是 `O(总字符数)`，`put`/`get`/`delete` 为 `O(1)`；空间 `O(总字符数)`。

**易错点。**
- 用分隔符拼接：`";".join(f"{k}={v}")`，`put("x=y", "z")` 的快照是 `x=y=z`，按第一个 `=` 拆回来得到 key `x`、value `y=z`，不是原数据。
- 长度和内容的单位不一致：长度用字符数，内容却按字节切片（或反过来），含中文、表情符号时位置错位。统一用 `str`，或统一用 `bytes`。
- `restore` 边解析边写入：数据在中间损坏，存储已经被改了一半。先解析到临时字典，成功后一次性替换。
- `snapshot()` 直接返回内部字典（或它的浅拷贝）：`s = kv.snapshot()` 之后 `kv.put("z", "9")`，`s` 里也出现 `z`。快照必须是不可变的字符串。

**追问。**
- 值是任意类型（嵌套）：每个值前加一个类型标签（`s` 字符串、`i` 整数、`l` 列表……），或者对整体使用 JSON，说明 JSON 的限制（键必须是字符串）。
- 增量快照 / 版本：记录写入日志，快照保存某个日志位置；或者用写时复制（copy-on-write）的持久化结构共享未改动的部分。
- 数据大、不能一次性放进内存：`snapshot` 做成生成器 `yield` 一块一块写出，`restore` 从文件流逐块读取。

**同模式。** LC 297 二叉树的序列化与反序列化、LC 449 序列化和反序列化二叉搜索树、LC 271 字符串的编码与解码、LC 535 TinyURL 的加密与解密。
