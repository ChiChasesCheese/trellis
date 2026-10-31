---
id: tlc-split-message-based-on-limit-0-whole
node: b.split-message-based-on-limit
type: qa
---
## Q
**LC 2468 根据限制分割消息**｜Hard · LC TikTok 全时段热度 50/100

给字符串 `message` 和正整数 `limit`。把 `message` 分割成一个或多个部分，每个部分的结尾都是 `"<a/b>"`：`b` 是分割出的总段数，`a` 是当前段的编号（从 `1` 到 `b`）。除了最后一段的长度可以小于等于 `limit` 之外，其他每一段（包括结尾）的长度都必须**等于** `limit`。删掉每段的结尾并按顺序连接，必须得到 `message`。结果数组要尽可能短。返回分割后的数组；无法分割就返回空数组。`1 <= message.length <= 10^4`，`message` 只含小写英文字母和空格，`1 <= limit <= 10^4`。例：`message = "short message"`，`limit = 15` → `["short mess<1/2>","age<2/2>"]`；`message = "this is really a very awesome message"`，`limit = 9` → 14 段，前三段是 `["thi<1/14>","s i<2/14>","s r<3/14>"]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先确定总段数 `b`：`b` 越大，后缀 `"<a/b>"` 越长，每段装的字符越少，所以从 `b = 1` 起依次尝试，第一个“总容量 `>= len(message)`”的 `b` 就是最短的；容量等于 `b · (limit - 3 - len(b)) - (编号 1..b 的位数之和)`，位数之和边枚举边累加。确定 `b` 后固定后缀，从左到右切：每段取 `limit - len(后缀)` 个字符，最后一段取剩余。`O(n)`。

**识别。** 「结果要最短」而且「每段的后缀长度依赖总段数」，是先定总段数、再构造的信号。后缀长度只随位数变化：`a` 是 `1..9` 时一位，`10..99` 时两位，以此类推，容量可以用算术累加算出，不必真的切。枚举 `b` 的上界是 `n`，因为每段至少装一个字符。

**推导。** 暴力：对每个 `b` 实际构造并验证，`O(n)` 每个，总 `O(n^2)`，`n = 10^4` 时约 `10^8`。浪费：判断某个 `b` 是否可行只需要总容量，不需要真的切。洞察：第 `a` 段的后缀长度是 `3 + len(a) + len(b)`，可装 `limit - 3 - len(a) - len(b)` 个字符，求和得 `b · (limit - 3 - len(b)) - Σ len(a)`。`Σ len(a)` 随 `b` 增加一项，`O(1)` 更新。无解的情形：最后一段（编号位数与 `b` 的位数相同）连一个字符都装不下，即 `limit - 3 - 2 · len(b) <= 0`，更大的 `b` 只会更糟，直接返回空数组。

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

运行：`("short message", 15)` → `['short mess<1/2>', 'age<2/2>']`；`("this is really a very awesome message", 9)` → `14` 段，前三段 `['thi<1/14>', 's i<2/14>', 's r<3/14>']`；`("abc", 5)` → `[]`（后缀 `"<1/1>"` 已占满 `5`）；`("abc", 6)` → `['a<1/3>', 'b<2/3>', 'c<3/3>']`；`("a", 6)` → `['a<1/1>']`；`10^4` 个字符、`limit = 12` → `8893` 段；`limit = 100` → `109` 段，均不到 `1 ms`。

**复杂度。** 时间 `O(n)`（枚举至多 `n` 个 `b`，构造 `O(n)`）；空间 `O(n)`（输出）。

**易错点。**
- 把所有编号都按一位数估算容量：`("this is really a very awesome message", 9)` 算出 `13` 段，正确是 `14` 段，因为编号 `10..14` 是两位数，后缀更长，每段装得更少。
- 无解时不返回空数组：`("abc", 5)` 里任何后缀都至少 `5` 个字符，正文装不下一个字符，必须返回 `[]`，而不是造出正文为空的段。
- 最后一段也当成必须填满 `limit`：最后一段只取剩余字符，切片 `message[pos:pos + take]` 在末尾自然截断。

**追问。**
- 总段数能不能不逐个枚举：按 `b` 的位数分组，每组内容量随 `b` 严格递增，对每组二分，只需要常数个组（见另一种解法）。
- 消息是流式的，不知道总长：总段数要等到全部读完才知道，要么缓存全部再切，要么在后缀里为 `b` 预留固定宽度（例如固定 5 位）。
- 要求每段正文至少 `m` 个字符：把无解判断改成 `limit - 3 - 2 · len(b) < m`，容量公式里的每段下限同步调整。

**同模式。** LC 68 文本左右对齐、LC 6 Z 字形变换、LC 1055 形成字符串的最短路径、LC 2109 向字符串添加空格。
