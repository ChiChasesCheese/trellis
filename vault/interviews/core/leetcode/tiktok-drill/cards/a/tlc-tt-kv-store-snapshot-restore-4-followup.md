---
id: tlc-tt-kv-store-snapshot-restore-4-followup
node: a.tt-kv-store-snapshot-restore
type: qa
step: 4
---
## Q
**带快照与恢复的内存键值存储**｜追问

键值存储的快照已经用「长度前缀」字符串实现。面试官接着问：（1）要输出二进制（`bytes`）格式，该注意什么？（2）值可以是整数、列表等嵌套类型？（3）怎样发现快照被篡改或截断？（4）数据很大，不能一次放进内存？

## A
1. **二进制**：长度必须是**字节数**，不是字符数。字符串先 `encode("utf-8")`，再用定长的大端整数 `struct.pack(">I", len(raw))` 写长度（四字节，不用冒号分隔，也就不会和内容冲突）。

```python
import struct


def dump(data: dict[str, str]) -> bytes:
    out = [struct.pack(">I", len(data))]
    for key, value in data.items():
        for s in (key, value):
            raw = s.encode("utf-8")                    # 长度必须是字节数，不是字符数
            out.append(struct.pack(">I", len(raw)) + raw)
    return b"".join(out)
```

   `dump({"k": "中"})` → `b'\x00\x00\x00\x01\x00\x00\x00\x01k\x00\x00\x00\x03\xe4\xb8\xad'`（`"中"` 一个字符、三个字节）。
2. **嵌套类型**：每个值前加一个类型标签（字符串、整数、列表……），列表递归地写“个数加各元素”；或者说明直接用 JSON，限制是键必须是字符串。
3. **校验**：头部加魔数和版本号，尾部加 `zlib.crc32` 校验和；`restore` 先验长度和校验和，再解析。条目数加“读完位置必须等于总长度”能发现截断和多余数据。
4. **大数据**：`snapshot` 做成生成器，一块一块 `yield`，写进文件；`restore` 用流逐块读取并保持“长度加内容”的解析状态；快照期间还有写入，就先对字典做一次浅拷贝（或写时复制），再序列化拷贝。

**Python 提醒**：`len(s)` 是字符数，`len(s.encode())` 才是 UTF-8 字节数，`"中"` 分别是 `1` 和 `3`；`struct.unpack_from(">I", blob, pos)` 从偏移处读取，不需要先切片。
