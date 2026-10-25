---
id: tlc-split-message-based-on-limit-5-alt
node: b.split-message-based-on-limit
type: qa
step: 5
---
## Q
**LC 2468 根据限制分割消息**｜另一种解法

不逐个枚举总段数 `b`，而是按 `b` 的位数分组、组内二分，怎么写？什么时候选它，什么时候选逐个枚举？

## A
**按位数分组加二分。** 总段数 `b` 的位数 `d` 固定时，容量函数 `cap(b) = b · (limit - 3 - d) - Σ_{a=1..b} len(a)`，其中 `Σ len(a)` 有闭式：每个位数 `e` 贡献 `e × (该位数范围内不超过 b 的编号个数)`。组内每多一段，容量增加 `limit - 3 - 2d`（后缀最长的一段），只要这个数为正，容量严格递增，可以二分。对 `d = 1, 2, …` 依次处理，第一个存在可行 `b` 的组里取最小的 `b`。

```python
from bisect import bisect_left


def cap_of(b: int, limit: int) -> int:
    """总段数为 b 时，所有段合计能装的字符数。"""
    digits_b = len(str(b))
    index_digits = sum(d * (min(b, 10**d - 1) - 10 ** (d - 1) + 1) for d in range(1, digits_b + 1))
    return b * (limit - 3 - digits_b) - index_digits


def split_message_alt(message: str, limit: int) -> list[str]:
    n = len(message)
    for digits_b in range(1, len(str(n)) + 1):
        lo, hi = 10 ** (digits_b - 1), min(10 ** digits_b - 1, n)
        if lo > hi or limit - 3 - 2 * digits_b <= 0:       # 这一组里每段连 1 个字符都装不下，更长的组更不行
            break
        b = lo + bisect_left(range(lo, hi + 1), n, key=lambda x: cap_of(x, limit))
        if b <= hi:                                        # 本组内存在容量 >= n 的 b，取最小
            out, pos = [], 0
            for a in range(1, b + 1):
                tail = f"<{a}/{b}>"
                take = limit - len(tail)
                out.append(message[pos:pos + take] + tail)
                pos += take
            return out
    return []
```

运行：`("short message", 15)` → `['short mess<1/2>', 'age<2/2>']`，`("this is really a very awesome message", 9)` → `14` 段，`("abc", 5)` → `[]`，`("a", 6)` → `['a<1/1>']`；与逐个枚举的结果完全一致，`10^4` 个字符、`limit = 12` 时找到 `b = 8893`。

**复杂度。** 找 `b`：至多 `len(str(n))` 个组，每组一次二分，每次容量计算 `O(位数)`，合计 `O(log^2 n)`；构造输出仍是 `O(n)`。

**什么时候选哪种。** `n <= 10^4` 时逐个枚举的 `O(n)` 已经与输出同阶，代码短、易验证，应当作主解法。分组二分只在“只需要段数、不需要构造输出”或 `n` 很大（如 `10^9`）时才值得，代价是闭式求和与组边界的细节容易写错。
