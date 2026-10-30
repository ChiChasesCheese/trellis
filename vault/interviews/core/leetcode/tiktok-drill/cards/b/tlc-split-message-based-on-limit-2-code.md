---
id: tlc-split-message-based-on-limit-2-code
node: b.split-message-based-on-limit
type: qa
step: 2
---
## Q
**LC 2468 根据限制分割消息**｜写出 Python 实现

字符串 `message`（小写字母和空格，长度 `1..10^4`）和正整数 `limit`（`1..10^4`）。分成最少的若干段，每段结尾是 `"<a/b>"`（`a` 为编号，`b` 为总段数），除最后一段可以更短外每段长度恰好是 `limit`，去掉结尾拼接回 `message`。无法分割返回 `[]`。

## A
**思路。** 枚举总段数 `b`，容量 = `b · (limit - 3 - len(b)) - 编号位数之和`；第一个容量 `>= n` 的 `b` 即最少段数。若最后一段（编号位数最多）的正文容量 `<= 0` 则无解。确定 `b` 后用格式化字符串生成后缀，按 `limit - len(后缀)` 切片。

```python
def split_message(message: str, limit: int) -> list[str]:
    n = len(message)
    total_parts = 0
    index_digits = 0                       # 编号 1..b 的位数总和
    for b in range(1, n + 1):              # 每段至少装 1 个字符，所以 b <= n
        index_digits += len(str(b))
        suffix = 3 + len(str(b))           # "<", "/", ">" 加上总段数 b 的位数
        capacity = b * (limit - suffix) - index_digits    # b 段一共能装的字符数
        if limit - suffix - len(str(b)) <= 0:             # 连最后一段（编号位数最多）都装不下 1 个字符
            return []
        if capacity >= n:
            total_parts = b
            break
    else:
        return []
    out: list[str] = []
    pos = 0
    for a in range(1, total_parts + 1):
        tail = f"<{a}/{total_parts}>"
        take = limit - len(tail)           # 除最后一段外都刚好填满 limit
        out.append(message[pos:pos + take] + tail)
        pos += take
    return out
```

运行：`("short message", 15)` → `['short mess<1/2>', 'age<2/2>']`；`("this is really a very awesome message", 9)` → `14` 段，前三段 `['thi<1/14>', 's i<2/14>', 's r<3/14>']`；`("abc", 5)` → `[]`；`("abc", 6)` → `['a<1/3>', 'b<2/3>', 'c<3/3>']`；`("a", 6)` → `['a<1/1>']`；`10^4` 个字符、`limit = 12` → `8893` 段，不到 `1 ms`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`。

**写法要点。** `for … else`：循环正常结束（没有 `break`）说明所有 `b <= n` 都装不下，直接返回 `[]`；`f"<{a}/{total_parts}>"` 一次生成后缀，用 `len(tail)` 取长度，不手算位数；`index_digits` 累加比每次重新求和快；切片 `message[pos:pos + take]` 越过末尾会自动截断，最后一段不用特判。
