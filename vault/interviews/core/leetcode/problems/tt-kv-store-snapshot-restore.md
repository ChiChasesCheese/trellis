---
slug: tt-kv-store-snapshot-restore
---
## Q
**带快照与恢复的内存键值存储**｜Medium

实现 `KVStore`：`put`、`get`（不存在返回 `None`）、`delete`（成功返回 `True`），再加 `snapshot()` 把全部数据序列化成字符串、`restore(data)` 恢复到快照时刻。不能用 `json` / `pickle`；key、value 可含任意字符；数据损坏抛 `ValueError` 且原存储不变。

## A
**一句话。** 长度前缀（length-prefix）编码：每个字符串写成 `长度:内容`，解码按长度取，不怕内容含分隔符；`restore` 先解析到临时字典，成功才替换。

```python
def enc(s):
    return f"{len(s)}:{s}"

def read(data, pos):
    colon = data.find(":", pos)
    if colon == -1 or not data[pos:colon].isdecimal():
        raise ValueError("bad length")
    end = colon + 1 + int(data[pos:colon])
    if end > len(data):
        raise ValueError("truncated")
    return data[colon + 1:end], end

class KVStore:
    def __init__(self):
        self.data = {}

    def put(self, k, v):
        self.data[k] = v

    def get(self, k):
        return self.data.get(k)

    def delete(self, k):
        return self.data.pop(k, None) is not None

    def snapshot(self):     # 条目数，然后 key、value 依次
        parts = [enc(str(len(self.data)))]
        for k, v in self.data.items():
            parts += [enc(k), enc(v)]
        return "".join(parts)

    def restore(self, snap):
        cnt, pos = read(snap, 0)
        if not cnt.isdecimal():
            raise ValueError("bad count")
        loaded = {}             # 先写临时字典
        for _ in range(int(cnt)):
            k, pos = read(snap, pos)
            v, pos = read(snap, pos)
            loaded[k] = v
        if pos != len(snap):
            raise ValueError("trailing data")
        self.data = loaded
```

**复杂度。** 时间 `snapshot`/`restore` 为 `O(总字符数)`、其余 `O(1)`，空间 `O(总字符数)`。

**易错点。**
- 用分隔符拼接：`put("x=y", "z")` 的快照 `x=y=z` 拆回来 key 成了 `x`。
- `restore` 边解析边写入：数据中途损坏，存储已被改一半。
- 长度按字符数、内容却按字节切：含中文、表情符号时错位，要统一用 `str`。

**追问。**
- 值是嵌套类型？：每个值前加类型标签（`s`、`i`、`l`……）。
- 数据太大？：`snapshot` 写成生成器分块输出，`restore` 从流里逐块读。

**同模式。** LC 297 二叉树的序列化与反序列化、LC 449 序列化和反序列化二叉搜索树、LC 271 字符串的编码与解码、LC 535 TinyURL 的加密与解密
