---
id: tlc-minimum-operations-to-make-character-frequencies-equal-5-alt
node: a.minimum-operations-to-make-character-frequencies-equal
type: qa
step: 5
---
## Q
**LC 3389 使字符频率相等的最少操作次数**｜另一种解法

不做枚举 `t` 加两状态 DP，直接按定义搜索怎么写？它适用于什么规模，为什么仍然值得会写？

## A
**思路。** 把字符串压缩成「各字母出现次数」的向量，每次操作就是向量上的一步：某一项 `-1`（删）、`+1`（补）、或把一项的 `1` 挪给下一项。从初始向量出发做广度优先搜索（BFS），第一次遇到「非零项全相等」的向量，步数就是答案。为了让状态有限，限制总长度不超过 `2n + 2`，字母表也缩小到前几个字母。

```python
from collections import deque


def make_string_good_bfs(s: str, letters: int = 6) -> int:
    start = tuple(s.count(chr(97 + i)) for i in range(letters))   # 只记每个字母的出现次数
    limit = 2 * len(s) + 2                       # 总长度封顶，防止"补字符"无限扩张
    dist = {start: 0}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if len({c for c in state if c}) <= 1:    # 所有出现过的字母次数相等（或只剩一种）：好字符串
            return dist[state]
        for i, c in enumerate(state):
            nexts: list[tuple[int, ...]] = []
            if c:                                # 删一个
                nexts.append(state[:i] + (c - 1,) + state[i + 1:])
            if sum(state) < limit:               # 补一个
                nexts.append(state[:i] + (c + 1,) + state[i + 1:])
            if c and i + 1 < letters:            # 把一个 i 变成 i+1
                nexts.append(state[:i] + (c - 1, state[i + 1] + 1) + state[i + 2:])
            for nxt in nexts:
                if nxt not in dist:
                    dist[nxt] = dist[state] + 1
                    queue.append(nxt)
    return -1
```

`"acab"` → `1`；`"wddw"` → `0`；`"aaabc"` → `2`。

**取舍。** 状态数随字符串长度和字母个数指数增长，只适合长度不超过 6、字母不超过 6 个的小例子。但它直接对应题意，没有任何推导，写出来就是对的，面试里可以作为「先保证正确」的第一版，或者在写完 `O(26M)` 解法后拿来在小输入上对照。正式解答（`n = 2 * 10^4`）必须用枚举 `t` 加两状态 DP。
