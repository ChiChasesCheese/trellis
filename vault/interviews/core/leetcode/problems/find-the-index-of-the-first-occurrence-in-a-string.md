---
slug: find-the-index-of-the-first-occurrence-in-a-string
---
## Q
**LC 28 找出字符串中第一个匹配项的下标**｜Easy

返回 `needle` 在 `haystack` 中第一次出现的下标，没有返回 `-1`。

## A
**一句话。** KMP：先算 `needle` 每个前缀的最长相等前后缀，失配时只回退 `needle` 的指针。

```python
def str_str(haystack, needle):
    m = len(needle)
    fail = [0] * m             # needle[:i+1] 的最长相等前后缀长度
    k = 0
    for i in range(1, m):      # 自己匹配自己建表
        while k and needle[i] != needle[k]:
            k = fail[k - 1]
        if needle[i] == needle[k]:
            k += 1
        fail[i] = k
    k = 0                      # 已匹配 needle 的前 k 个字符
    for i, ch in enumerate(haystack):
        while k and ch != needle[k]:
            k = fail[k - 1]    # haystack 指针不回头
        if ch == needle[k]:
            k += 1
        if k == m:
            return i - m + 1
    return -1
```

**复杂度。** 时间 `O(n + m)`，空间 `O(m)`。

**易错点。**
- 失配回退写成 `k - 1`：`haystack="abba"`, `needle="aba"` 会错返回 `1`，应用 `fail[k-1]`。
- 建表时 `i` 从 `0` 开始：`needle[0]` 与自己比，`fail[0]` 变 `1`，真前缀定义被破坏。

**追问。**
- 面试里能不写 KMP 吗？：先说暴力 `O(nm)`，再说 KMP 的思路；简单场景直接 `haystack.find(needle)`。
- 不想建表有别的办法吗？：滚动哈希（Rabin-Karp），哈希相同再逐字比对。

**同模式。** LC 459 重复的子字符串、LC 214 最短回文串、LC 686 重复叠加字符串匹配、LC 1392 最长快乐前缀
