---
slug: number-of-equivalent-domino-pairs
---
## Q
**LC 1128 等价多米诺骨牌对的数量**｜Easy

`dominoes[i] = [a, b]`，两块骨牌 `[a, b]` 和 `[c, d]` 等价当且仅当 `a == c, b == d` 或 `a == d, b == c`。统计满足 `i < j` 且 `dominoes[i]` 与 `dominoes[j]` 等价的 `(i, j)` 对数。

## A
**一句话。** 把每块牌规范成 `(min, max)`，用计数器边读边累加：每遇到一个，之前相同的每一块都能与它配对。

```python
def num_equiv_domino_pairs(dominoes):
    cnt, ans = Counter(), 0
    for a, b in dominoes:
        key = (min(a, b), max(a, b))   # 翻转后等价：规范成有序对
        ans += cnt[key]                # 之前每块相同的牌配成一对
        cnt[key] += 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先 `cnt[key] += 1` 再累加：会和自己配对，多算 `n` 对。
- 不规范化：`[1,2]` 与 `[2,1]` 当成不同牌，漏掉翻转等价。

**追问。**
- 先统计再套 `C(c, 2)` 行吗？：可以，每组数量 `c` 贡献 `c(c-1)/2`，结果相同。
- 值域是 `1..9` 怎么更快？：用 `a * 10 + b` 当键放进长度 100 的数组。

**同模式。** LC 1 两数之和、LC 750 角矩形的数量
