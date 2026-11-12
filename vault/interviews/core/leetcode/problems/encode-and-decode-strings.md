---
slug: encode-and-decode-strings
---
## Q
**LC 271 Encode and Decode Strings**｜Medium

把字符串列表编码成一个字符串，再解码回原列表；字符串可含任意字符，不许用 `eval` 等序列化方法。

## A
**一句话。** 长度前缀编码：每段写成 `长度#内容`，解码先读长度再按长度截取。

```python
class Codec:
    def encode(self, strs):
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s):
        strs, i = [], 0
        while i < len(s):
            j = s.index("#", i)       # 第一个 "#" 必是长度的结束符
            size = int(s[i:j])
            strs.append(s[j + 1:j + 1 + size])
            i = j + 1 + size
        return strs
```

**复杂度。** 时间 `O(总长度)`，空间 `O(总长度)`。

**易错点。**
- 用 `s.split("#")` 解码：内容里含 `#` 就错位，只能在读长度的位置找 `#`。
- 长度单位不一致：非 ASCII 时两端要统一用字符数或 UTF-8 字节数。
- 空串与空列表混淆：`[""]` 编码为 `"0#"`，`[]` 编码为 `""`，循环条件 `i < len(s)` 能区分。

**追问。**
- 为什么不用分隔符加转义？：可行，但多一个转义状态，长度前缀更简单。
- 流式读取怎么做？：先读定长头，再读 `size` 个字符，不必整体缓冲。

**同模式。** LC 297 二叉树的序列化与反序列化、LC 428 序列化和反序列化 N 叉树、LC 535 TinyURL 的加密与解密、LC 394 字符串解码
