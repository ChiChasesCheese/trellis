---
slug: longest-substring-of-one-repeating-character
---
## Q
**LC 2213 由单个字符重复的最长子字符串**｜Hard

字符串 `s`（长 `10^5`），`k` 次单点修改，每次修改后返回只含一种字符的最长子串长度。

## A
**一句话。** 线段树每个节点存「前缀同字符长、后缀同字符长、区间最长」，合并时若中缝两侧字符相同就把左后缀和右前缀拼起来；单点修改沿路径重算。

```python
def longest_repeating(s, query_characters, query_indices):
    s, n = list(s), len(s)
    pre, suf, best = [0] * 4 * n, [0] * 4 * n, [0] * 4 * n

    def pull(o, l, m, r):
        a, b = 2 * o, 2 * o + 1
        pre[o], suf[o] = pre[a], suf[b]
        best[o] = max(best[a], best[b])
        if s[m] == s[m + 1]:          # 中缝能接上
            if pre[a] == m - l + 1:   # 左半整段同字符
                pre[o] += pre[b]
            if suf[b] == r - m:
                suf[o] += suf[a]
            best[o] = max(best[o], suf[a] + pre[b])

    def build(o, l, r):
        if l == r:
            pre[o] = suf[o] = best[o] = 1
            return
        m = (l + r) // 2
        build(2 * o, l, m)
        build(2 * o + 1, m + 1, r)
        pull(o, l, m, r)

    def update(o, l, r, i):
        if l == r:
            return
        m = (l + r) // 2
        if i <= m:
            update(2 * o, l, m, i)
        else:
            update(2 * o + 1, m + 1, r, i)
        pull(o, l, m, r)

    build(1, 0, n - 1)
    ans = []
    for c, i in zip(query_characters, query_indices):
        s[i] = c
        update(1, 0, n - 1, i)
        ans.append(best[1])
    return ans
```

**复杂度。** 时间 `O(n + k log n)`，空间 `O(n)`。

**易错点。**
- 合并时无条件 `pre[o] = pre[a] + pre[b]`：只有左半整段同字符时前缀才能延伸到右半。
- 每次修改后整串重扫：`O(nk)`，`10^10` 超时。

**追问。**
- 不用线段树？：有序集合维护「同字符段」的区间，修改时拆分合并，最长值用可删除的计数有序表维护，`O(log n)`。
- 中缝字符为什么直接读 `s[m]`、`s[m+1]`？：叶子就是原串，修改先写 `s` 再更新，读到的就是最新字符。

**同模式。** LC 307 区域和检索 - 数组可修改、LC 53 最大子数组和、LC 1446 连续字符
