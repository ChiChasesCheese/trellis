---
id: tlc-longest-string-chain-4-followup
node: p5.longest-string-chain
type: qa
step: 4
---
## Q
**LC 1048 最长字符串链**｜追问

面试官接着问：（1）要返回具体的那条最长词链？（2）用记忆化递归写？（3）单词多、长度也大，切片太慢怎么办？分别怎么改。

## A
1. **返回词链**：多存一个 `prev: dict[str, str]`，记录取得最大值的那个候选；找到 `dp` 最大值对应的单词 `w`，沿 `prev` 不断往回走，最后反转。

```python
def longest_chain_words(words: list[str]) -> list[str]:
    dp: dict[str, int] = {}
    prev: dict[str, str] = {}
    for w in sorted(words, key=len):
        dp[w] = 1
        for i in range(len(w)):
            p = w[:i] + w[i + 1:]
            if dp.get(p, 0) + 1 > dp[w]:
                dp[w] = dp[p] + 1
                prev[w] = p
    cur = max(dp, key=dp.get)
    chain = [cur]
    while cur in prev:
        cur = prev[cur]
        chain.append(cur)
    return chain[::-1]
```

   `["a","b","ba","bca","bda","bdca"]` 得到 `['a', 'ba', 'bca', 'bdca']`（长度同为 `4` 的链有多条，取先遇到的）。
2. **记忆化递归**：`go(w)` 返回以 `w` 结尾的最长链，`go(w) = 1 + max(go(p) for p in 候选 if p in 单词集合)`，用 `functools.cache` 缓存；不需要排序，递归深度至多 `16`（每层单词短一个字母），很安全。
3. **加速**：切片的代价是 `O(L)`。可以把每个单词的「通配符桶」（删去第 `i` 个字母，如 `"b*a"`）建倒排索引，或者用字典树，只比较可能匹配的词；在 `L = 16`、`N = 1000` 时没有必要，规模大到 `10^5` 个词再考虑。

**Python 提醒**：`max(dp, key=dp.get)` 遍历字典的键并用 `dp.get` 取值，返回值最大的键；多个并列时返回第一个遇到的键。`dp.get(p, 0)` 与 `dp[p]` 不能混用：键不存在时后者抛 `KeyError`。
