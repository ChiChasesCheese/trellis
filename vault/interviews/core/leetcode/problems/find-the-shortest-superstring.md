---
slug: find-the-shortest-superstring
---
## Q
**LC 943 最短超级串**｜Hard

给互不相同的字符串数组 `words`（`n ≤ 12`，其中没有字符串是另一个的子串），返回包含所有 `words[i]` 作为子串的最短字符串，答案不唯一时返回任意一个。

## A
**一句话。** 先算出任意两词的重叠长度，问题变成最短哈密顿路径：状态压缩 DP，`f[mask][j]` 是覆盖 `mask`、以 `j` 结尾时能省下的最大重叠，再回溯拼接。

```python
def shortest_superstring(words):
    n = len(words)
    def overlap(a, b):               # a 的后缀 = b 的前缀 的最长长度
        for k in range(min(len(a), len(b)) - 1, 0, -1):
            if a.endswith(b[:k]):
                return k
        return 0
    ov = [[overlap(a, b) for b in words] for a in words]
    # f[mask][j]：覆盖 mask、以 j 结尾，省下的最大长度
    f = [[-1] * n for _ in range(1 << n)]
    pre = [[-1] * n for _ in range(1 << n)]
    for j in range(n):
        f[1 << j][j] = 0
    for mask in range(1 << n):
        for i in range(n):
            if f[mask][i] < 0:
                continue
            for j in range(n):
                if mask >> j & 1:
                    continue
                nm, v = mask | 1 << j, f[mask][i] + ov[i][j]
                if v > f[nm][j]:
                    f[nm][j], pre[nm][j] = v, i
    mask = (1 << n) - 1
    j = max(range(n), key=lambda j: f[mask][j])
    order = []
    while j >= 0:                    # 沿前驱回溯得到顺序
        order.append(j)
        mask, j = mask ^ (1 << j), pre[mask][j]
    order.reverse()
    res = words[order[0]]
    for a, b in zip(order, order[1:]):
        res += words[b][ov[a][b]:]   # 只拼上不重叠的部分
    return res
```

**复杂度。** 时间 `O(2^n · n²)`，空间 `O(2^n · n)`。

**易错点。**
- 把重叠取成整个较短串：重叠必须小于较短串长度，`k` 从 `min(len) - 1` 开始。
- 用贪心每次拼重叠最大的一对：局部最优不是全局最优，要枚举顺序，即最短哈密顿路径。
- 回溯时 `mask` 和 `j` 的更新顺序错：右边先算出旧 `mask` 下的前驱，元组赋值保证这一点。

**追问。**
- 为什么「最短」等价于「重叠和最大」？：串长 = 各词长度之和 − 相邻重叠和，长度和固定。
- 有子串关系的词怎么办？：先删掉被别的词包含的词，否则重叠模型不成立。

**同模式。** LC 847 访问所有节点的最短路径、LC 1125 最小的必要团队、LC 980 不同路径 III
