---
id: tlc-longest-common-prefix-4-followup
node: a.longest-common-prefix
type: qa
step: 4
---
## Q
**LC 14 最长公共前缀**｜追问

面试官接着问：（1）有没有只比较两个字符串的更短写法？（2）Python 标准库里有现成函数吗？（3）字符串很多、要反复查询怎么办？

## A
1. **最小 / 最大。** 字典序最小和最大的两个串的公共前缀，就是全体的公共前缀（中间的串夹在两者之间，必然以这个前缀开头）：

```python
def longest_common_prefix_minmax(strs: list[str]) -> str:
    lo, hi = min(strs), max(strs)                # 字典序最小和最大的两个串，公共前缀就是全体的公共前缀
    for i, (a, b) in enumerate(zip(lo, hi)):
        if a != b:
            return lo[:i]
    return lo
```

`["flower","flow","flight"]` → `"fl"`；`["dog","racecar","car"]` → `""`。
2. **标准库。** `os.path.commonprefix(strs)` 按**字符**逐位比较，结果和上面一致；名字里有 `path`，但它并不按路径分隔符拆分，在面试里直接调用等于没有回答题目，只适合作为对照。
3. **反复查询。** 把字符串建成 Trie，公共前缀就是从根出发、沿着唯一孩子一路走、直到出现分叉或某个单词结束为止的那条路径；多次对不同子集查询时可以按需扩展。

**Python 提醒**：`min(strs)` 和 `max(strs)` 对字符串按字典序比较，是 `O(S)`；当列表为空时会抛 `ValueError`，这里保证至少有一个字符串。
