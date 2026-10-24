---
id: tlc-word-break-2-code
node: b.word-break
type: qa
step: 2
---
## Q
**LC 139 单词拆分**｜写出 Python 实现

字符串 `s`（长度 `1..300`）与字符串列表 `wordDict`（`1..1000` 个互不相同的小写单词，每个长度 `1..20`）。若 `s` 能由字典中的单词（可重复使用）拼接而成，返回 `True`，否则返回 `False`。

## A
**思路。** `dp[i]` 表示 `s[:i]` 能否被拆分，`dp[0] = True`。对每个 `i`，在最近 `max_len` 个切点 `j` 里找一个 `dp[j]` 为真且 `s[j:i]` 在字典里的；找到就是真。结果是 `dp[-1]`。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)                       # 哈希集合：判断"切片是不是单词"是 O(L)
    max_len = max(map(len, words))               # 单词最长 max_len，更长的切片不用试
    dp = [True] + [False] * len(s)               # dp[i]：前 i 个字符 s[:i] 能否被拆成单词
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(max(0, i - max_len), i))
    return dp[-1]
```

**运行。** `("leetcode", ["leet","code"])` → `True`；`("applepenapple", ["apple","pen"])` → `True`；`("catsandog", ["cats","dog","sand","and","cat"])` → `False`；`("a", ["b"])` → `False`；`("aaaaaaa", ["aaaa","aaa"])` → `True`。

**复杂度。** 时间 `O(n · L²)`：`n` 个位置、每个至多 `L` 个切点，每次切片与哈希查找 `O(L)`；空间 `O(n)` 加字典本身。

**写法要点。** `set` 把查找从 `O(|dict|)` 降到 `O(L)`；`max(map(len, words))` 取最长单词，用来限制切点范围；`any(生成器)` 在找到第一个真值时短路，`dp[j] and …` 先判断便宜的布尔值再切片；`[True] + [False] * len(s)` 一步建好带哨兵的表；`range(max(0, i - max_len), i)` 防止下标为负。
