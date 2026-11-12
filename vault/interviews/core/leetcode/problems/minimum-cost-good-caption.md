---
slug: minimum-cost-good-caption
---
## Q
**LC 3441 变成好标题的最少代价**｜Hard

字符串 `caption` 每次可把一个字符改成相邻字母，求变成「每个字符都在连续至少 3 个相同字符的一组里」的最少操作数；并列取字典序最小，做不到返回 `""`。

## A
**一句话。** 从右往左 DP 算每个状态（字母、连续长度 1/2/≥3）补完的最小代价，再从左往右逐位贪心取最小字母。

```python
INF = 10**9

def min_cost_good_caption(caption):
    n = len(caption)
    if n < 3:
        return ""
    cap = [ord(ch) - 97 for ch in caption]
    W = 78                    # 每位 26 字母 × 3 档连续长度
    # h[i*W + c*3 + r]：第 i 位是 c、连续 r+1 个，补完右边的代价
    h = array("i", [INF]) * (n * W)
    for c in range(26):
        h[(n - 1) * W + c * 3 + 2] = 0   # 末位须已连续 ≥3
    for i in range(n - 2, -1, -1):
        nxt = (i + 1) * W
        cost = [abs(cap[i + 1] - c) for c in range(26)]
        # 换字母：取最小和次小，用来排除 c' == c
        g = sorted((cost[c] + h[nxt + c * 3], c)
                   for c in range(26))
        (g1, c1), (g2, _) = g[0], g[1]
        for c in range(26):
            base = i * W + c * 3
            for r in range(3):
                k = nxt + c * 3 + min(r + 1, 2)
                stay = cost[c] + h[k]
                # 连续 ≥3 才能换字母
                sw = INF
                if r == 2:
                    sw = g2 if c == c1 else g1
                h[base + r] = min(stay, sw, INF)

    best = min(abs(cap[0] - c) + h[c * 3]
               for c in range(26))
    if best >= INF:
        return ""
    out = []
    acc, cur, run = 0, -1, 0   # 已花代价、上个字母、连续档位
    for i in range(n):
        for c in range(26):    # 从 'a' 试起得字典序最小
            if i == 0:
                r = 0
            elif c == cur:
                r = min(run, 2)
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

**复杂度。** 时间 `O(26n)`，空间 `O(78n)`。

**易错点。**
- 连续不足 3 就换字母：`"abcabc"` 会原样返回，应为 `"bbbbbb"`。
- 并列时没取字典序最小：`"cdcd"` 返回 `"dddd"`，应为 `"cccc"`；重建要从 `'a'` 试，以等于全局最小为准。
- `INF` 与代价相加溢出 32 位：每步 `min(…, INF)` 截断，`n < 3` 先返回 `""`。

**追问。**
- 把「至少 3 次」改成「至少 `k` 次」？：长度档位封顶到 `k`，状态 `26k` 每位，`O(26nk)`。
- 只要最少操作数？：块长只需考虑 3、4、5，块内改成中位字母，`O(n)`。

**同模式。** LC 1473 粉刷房子 III、LC 2478 完美分割的方案数、LC 1220 统计元音字母序列的数目
