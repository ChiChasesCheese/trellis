---
id: tlc-scramble-string-2-code
node: b.scramble-string
type: qa
step: 2
---
## Q
**LC 87 扰乱字符串**｜写出 Python 实现

两个等长的小写字符串 `s1`、`s2`（长度 `1` 到 `30`）。扰乱：任选位置切成两个非空段，可以交换两段，再对两段递归扰乱。判断 `s2` 能否由 `s1` 扰乱得到。

## A
**思路。** `dfs(i, j, L)`：`s1[i:i+L]` 能否扰乱成 `s2[j:j+L]`。两段相等返回 `True`，字符计数不同返回 `False`；否则枚举切点 `k`，检查「不交换」和「交换」两种对应关系，有一种成立即可。

```python
from collections import Counter
from functools import cache


def is_scramble(s1: str, s2: str) -> bool:
    @cache
    def dfs(i: int, j: int, length: int) -> bool:
        # s1[i : i+length] 能否扰乱成 s2[j : j+length]
        a, b = s1[i:i + length], s2[j:j + length]
        if a == b:
            return True
        if Counter(a) != Counter(b):                      # 字符多重集不同，一定不行（剪枝）
            return False
        for k in range(1, length):                        # s1 这段在第 k 个字符后切开
            # 不交换：前 k 个对 s2 的前 k 个，后段对后段
            if dfs(i, j, k) and dfs(i + k, j + k, length - k):
                return True
            # 交换：s1 的前 k 个对 s2 的后 k 个，s1 的后段对 s2 的前段
            if dfs(i, j + length - k, k) and dfs(i + k, j, length - k):
                return True
        return False

    return dfs(0, 0, len(s1))
```

运行：`"great", "rgeat"` → `True`，`"abcde", "caebd"` → `False`，`"a", "a"` → `True`，`"abc", "bca"` → `True`，`"abcd", "bdac"` → `False`。

**复杂度。** 时间 `O(n^4)`：`O(n^3)` 个状态，每个枚举 `O(n)` 个切点，另有 `O(n)` 的切片和计数；空间 `O(n^3)`，递归深度不超过 `n`。

**写法要点。** 内部函数加 `@functools.cache` 自动按参数记忆化，参数用整数下标而不是子串，键更小；`Counter(a) != Counter(b)` 一行完成多重集比较；`and` 短路，左半不成立时不会去算右半；嵌套函数直接读外层的 `s1`、`s2`，每次调用 `is_scramble` 都是新的缓存，不会串用。
