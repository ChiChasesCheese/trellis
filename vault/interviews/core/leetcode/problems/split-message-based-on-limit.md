---
slug: split-message-based-on-limit
---
## Q
**LC 2468 根据限制分割消息**｜Hard

把 `message` 切成最少的若干段，每段结尾为 `"<a/b>"`（`a` 是编号，`b` 是总段数）；除最后一段可以更短外，每段总长必须恰好等于 `limit`。无法切分返回空数组。

## A
**一句话。** 枚举总段数 `b`，第一个总容量够装下整条消息的 `b` 就是最少段数，再按固定后缀从左到右切。

```python
def split_message(message, limit):
    n = len(message)
    digits = 0                    # 编号 1..b 的位数之和
    parts = 0
    for b in range(1, n + 1):
        digits += len(str(b))
        suf = 3 + len(str(b))     # "<", "/", ">" 加 b 的位数
        if limit - suf - len(str(b)) <= 0:
            return []             # 连一个字符都装不下
        if b * (limit - suf) - digits >= n:
            parts = b
            break
    else:
        return []
    out, pos = [], 0
    for a in range(1, parts + 1):
        tail = f"<{a}/{parts}>"
        take = limit - len(tail)
        out.append(message[pos:pos + take] + tail)
        pos += take
    return out
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 所有编号都按一位数估容量：`("this is really a very awesome message", 9)` 应为 `14` 段，编号 `10..14` 是两位数。
- 无解不返回 `[]`：`("abc", 5)` 后缀至少 5 字符，正文装不下，必须返回 `[]`。
- 最后一段也要填满：最后一段只取剩余字符，切片自然截断。

**追问。**
- 能不枚举 `b` 吗？：按 `b` 的位数分组，组内容量随 `b` 递增，对每组二分。

**同模式。** LC 68 文本左右对齐、LC 6 Z 字形变换、LC 2109 向字符串添加空格
