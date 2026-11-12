---
slug: word-pattern-ii
---
## Q
**LC 291 单词规律 II**｜Medium

给模式 `pattern` 和字符串 `s`，判断是否存在从模式字符到非空子串的双射，使得替换后恰好得到 `s`。

## A
**一句话。** 回溯：新字符枚举它对应 `s` 的哪一段，用 `used` 集合保证双射，失败就撤销。

```python
def word_pattern_match(pattern, s):
    mp, used = {}, set()
    def dfs(i, j):                   # pattern[i:] 匹配 s[j:]
        if i == len(pattern):
            return j == len(s)
        ch = pattern[i]
        if ch in mp:
            w = mp[ch]
            if not s.startswith(w, j):
                return False
            return dfs(i + 1, j + len(w))
        for end in range(j + 1, len(s) + 1):   # 非空
            w = s[j:end]
            if w in used:
                continue
            mp[ch] = w
            used.add(w)
            if dfs(i + 1, end):
                return True
            del mp[ch]               # 回溯
            used.remove(w)
        return False
    return dfs(0, 0)
```

**复杂度。** 时间 指数级（最坏约 `O(C(n-1, m-1))`），空间 `O(m)`。

**易错点。**
- 忘了 `used`：`"ab"` 配 `"aa"` 会让 `a`、`b` 都映射到 `"a"`，得 `True`，应为 `False`。
- 回溯只撤销 `mp` 不撤销 `used`（或相反）：后面的分支状态被污染。
- `end` 从 `j` 开始：允许映射到空串，题目要求非空。

**追问。**
- 只要单向映射、不要求双射？：去掉 `used`。
- 怎么剪枝？：剩余 `s` 长度小于剩余模式字符数时直接返回 `False`。

**同模式。** LC 290 单词规律、LC 205 同构字符串、LC 93 复原 IP 地址、LC 46 全排列
