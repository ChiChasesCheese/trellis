---
id: tlc-encode-and-decode-strings-0-whole
node: c.encode-and-decode-strings
type: qa
---
## Q
**LC 271 字符串的编码与解码**｜Medium · LC TikTok 全时段热度 26/100

设计算法把一个字符串列表编码成一个字符串（可以通过网络传输），接收端再解码回原来的列表。实现 `encode(strs)` 与 `decode(s)`，`decode(encode(strs))` 必须等于 `strs`。不允许使用任何序列化方法（如 `eval`）。`1 <= strs.length <= 200`，`0 <= strs[i].length <= 200`，`strs[i]` 可以包含 256 个有效 ASCII 字符中的任何字符。进阶：能否处理任意字符集。例：`["Hello","World"]` 编码再解码得到 `["Hello","World"]`；`[""]` 得到 `[""]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 长度前缀编码：每个字符串写成 `长度#内容`，解码时先读到 `#` 得到长度，再按长度截取内容，内容里是什么字符都不会被误判。

**识别。** 「把多个字符串拼成一个、还要无歧义拆开」：任何分隔符方案都会遇到「内容里恰好含有分隔符」，两条出路是转义，或者先声明长度。长度前缀不依赖字符集，是网络协议（如 HTTP chunked、Redis RESP）的常见做法。

**推导。** 朴素：用 `,` 拼接，内容含 `,` 就拆错。转义：把内容里的分隔符替换成转义序列，实现细节多。长度前缀：解码时读数字直到第一个 `#`，它一定是长度后面的分隔符（长度只含数字，内容在其后），然后跳过 `长度` 个字符，下一段从那里开始，内容里的 `#` 和数字都不会被解析。

```python
class Codec:
    def encode(self, strs: list[str]) -> str:
        return "".join(f"{len(s)}#{s}" for s in strs)    # 每段：长度 + "#" + 内容

    def decode(self, s: str) -> list[str]:
        strs: list[str] = []
        i = 0
        while i < len(s):
            j = s.index("#", i)                  # 从 i 起第一个 "#" 一定是长度的结束符
            size = int(s[i:j])
            strs.append(s[j + 1:j + 1 + size])   # 按长度截取，内容里有 "#" 或数字也不影响
            i = j + 1 + size                     # 跳到下一段的开头
        return strs
```

运行：`["Hello","World"]` 编码为 `"5#Hello5#World"`，解码得 `["Hello","World"]`；`[""]` 编码为 `"0#"`，解码得 `[""]`；`["3#a", "", "#"]` 编码为 `"3#3#a0#1##"`，解码还原；`[]` 编码为 `""`，解码得 `[]`。

**复杂度。** 时间 `O(总长度)`，空间 `O(总长度)`。

**拓展优化。**
- 任意字符集（二进制安全）：长度写成定长 4 字节大端整数，直接对 `bytes` 操作，不再依赖「`#`」。

```python
import struct


def encode_bytes(strs: list[bytes]) -> bytes:
    return b"".join(struct.pack(">I", len(s)) + s for s in strs)   # 4 字节大端长度 + 内容


def decode_bytes(data: bytes) -> list[bytes]:
    out: list[bytes] = []
    i = 0
    while i < len(data):
        (size,) = struct.unpack_from(">I", data, i)               # 读定长头
        out.append(data[i + 4:i + 4 + size])
        i += 4 + size
    return out
```

- 转义方案可作为备选：把内容中的 `/` 写成 `//`，每段以 `/:` 结尾，解码时遇到 `/` 看下一个字符；不需要先知道长度，适合流式写入。

**易错点。**
- 用 `s.split("#")` 解码：内容里含 `#` 时直接错位。必须只在读长度的位置找 `#`。
- 长度只算字符数不算字节数：传输编码非 ASCII 时，两端对「长度」的单位要一致（字符还是 UTF-8 字节）。
- 空字符串与空列表混淆：`[""]` 编码是 `"0#"`，`[]` 编码是 `""`，解码时循环条件 `i < len(s)` 能区分二者。

**追问。**
- 为什么不用 `,` 分隔再转义：可行，但转义逻辑多一个状态，长度前缀更简单。
- 超大字符串、流式读取：定长头加内容，读够头再读 `size` 个字节，不需要整体缓冲。

**同模式。** LC 297 二叉树的序列化与反序列化、LC 428 序列化和反序列化 N 叉树、LC 535 TinyURL 的加密与解密、LC 443 压缩字符串、LC 394 字符串解码。
