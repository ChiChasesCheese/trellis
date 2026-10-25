---
id: tlc-longest-string-chain-2-code
node: b.longest-string-chain
type: qa
step: 2
---
## Q
**LC 1048 最长字符串链**｜写出 Python 实现

小写单词数组 `words`（`1 <= words.length <= 1000`，`1 <= words[i].length <= 16`），`wordA` 是 `wordB` 的前身，当且仅当在 `wordA` 某处插入恰好一个字母可得 `wordB`。返回最长词链（每个单词是下一个的前身）的长度。

## A
**思路。** 按长度升序遍历单词。对单词 `w`，枚举删去第 `i` 个字母得到的候选串，在 `dp` 里查它们的最长链长度，取最大值加一。没有任何候选在表里就是 `1`。

```python
def longest_str_chain(words: list[str]) -> int:
    dp: dict[str, int] = {}                                  # dp[w]：以 w 结尾的最长词链
    for w in sorted(words, key=len):                         # 短的先处理，前身一定已算好
        dp[w] = 1 + max((dp.get(w[:i] + w[i + 1:], 0) for i in range(len(w))), default=0)
    return max(dp.values())
```

运行：`["a","b","ba","bca","bda","bdca"]` → `4`；`["xbc","pcxbcf","xb","cxbc","pcxbc"]` → `5`；`["abcd","dbqca"]` → `1`；`["a"]` → `1`；`["a","a"]` → `1`。

**复杂度。** 时间 `O(N log N + N * L^2)`：每个词 `L` 个候选，每个候选切片 `O(L)`；空间 `O(N * L)`。

**写法要点。** `sorted(words, key=len)` 用 `len` 当排序键，不修改原列表；`dp.get(候选, 0)` 把「候选不存在」和「长度为 `0`」合并；生成器表达式配合 `max(..., default=0)`，不构造中间列表，也不会在空序列上抛 `ValueError`；`w[:i] + w[i + 1:]` 是「删去第 `i` 个字母」的惯用写法。
