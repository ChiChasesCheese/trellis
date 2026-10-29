---
id: tlc-minimum-cost-good-caption-2-code
node: a.minimum-cost-good-caption
type: qa
step: 2
---
## Q
**LC 3441 变成好标题的最少代价**｜写出 Python 实现

长度 `1..5 * 10^4` 的小写字母串 `caption`。每个字符都在连续出现至少 3 次的一组里时是好标题。每次操作把一个字符改成前一个或后一个字母。返回最少操作次数对应的好标题，并列取字典序最小，无解返回 `""`。要求 `O(26n)`。

## A
**思路。** 反向 DP 求 `h[i][c][r]`：第 `i` 位定为字母 `c`、末尾连续 `r` 个（`1`、`2`、`>= 3`）时，补完右边的最小代价。换字母时用「最小和次小」排除同字母。然后正向贪心，从 `'a'` 到 `'z'` 逐位试，选第一个让「已花 + 本位 + `h`」等于全局最小的字母。

```python
from array import array

INF = 10**9


def min_cost_good_caption(caption: str) -> str:
    n = len(caption)
    if n < 3:
        return ""
    cap = [ord(ch) - 97 for ch in caption]
    W = 26 * 3                                   # 每个位置 78 个状态：(字母 c, 连续长度 r)，r = 1, 2, 3(表示 >= 3)
    # h[i*W + c*3 + (r-1)]：位置 i 已定为字母 c、末尾连续 r 个时，补完 i+1.. 的最小代价（补不成为 INF）
    h = array("i", [INF]) * (n * W)
    for c in range(26):
        h[(n - 1) * W + c * 3 + 2] = 0           # 最后一位只有连续长度 >= 3 才合法
    for i in range(n - 2, -1, -1):
        nxt = (i + 1) * W
        cost = [abs(cap[i + 1] - c) for c in range(26)]
        # 换字母的最优：min over c' of cost[c'] + h[i+1][c'][r=1]，保留最小和次小，用来排除 c' == c
        g = sorted((cost[c] + h[nxt + c * 3], c) for c in range(26))
        (g1, c1), (g2, _) = g[0], g[1]
        for c in range(26):
            base = i * W + c * 3
            for r in range(3):                   # r+1 为当前连续长度
                stay = cost[c] + h[nxt + c * 3 + min(r + 1, 2)]      # 接着写同一个字母
                switch = (g2 if c == c1 else g1) if r == 2 else INF  # 只有连续 >= 3 才能换字母
                h[base + r] = min(stay, switch, INF)

    # 从左到右贪心：每一位取最小的字母，只要"已花代价 + 这一位 + 补完"仍等于全局最小
    best = min(abs(cap[0] - c) + h[c * 3] for c in range(26))
    if best >= INF:
        return ""
    out: list[str] = []
    acc, cur, run = 0, -1, 0                     # 已花代价、上一个字母、连续长度(1,2,3)
    for i in range(n):
        for c in range(26):
            if i == 0:
                r = 0
            elif c == cur:
                r = min(run, 2)                  # 连续长度 run -> min(run+1, 3) 对应下标 min(run, 2)
            elif run == 3:
                r = 0
            else:
                continue
            step = abs(cap[i] - c)
            if acc + step + h[i * W + c * 3 + r] == best:
                out.append(chr(97 + c))
                acc, cur, run = acc + step, c, r + 1
                break
    return "".join(out)
```

**运行。** `"cdcd"` → `"cccc"`；`"aca"` → `"aaa"`；`"bc"` → `""`；`"aaa"` → `"aaa"`；`"abcabc"` → `"bbbbbb"`；`"zzzaaa"` → `"zzzaaa"`；`"zzzzy"` → `"zzzzz"`。

**复杂度。** 时间 `O(26n)`：反向 DP 每位 78 个状态、每个 `O(1)`，每位还要给 26 个转移排一次序；正向每位至多试 26 个字母；空间 `O(78n)` 个 32 位整数，约 15 MB。

**写法要点。** 状态压成一维 `array('i')`，比 `list[list[int]]` 省内存、访问快；`sorted((cost + h, c) …)` 只取前两项，26 个元素排序可以忽略，写法比手写「最小 / 次小」两个变量更不易错；`(g2 if c == c1 else g1)` 用最小 / 次小排除同字母；`min(stay, switch, INF)` 每步截断，防止 32 位溢出；重建用「等于全局最小」判断，不需要保存父指针。
