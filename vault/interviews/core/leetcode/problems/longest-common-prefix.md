---
slug: longest-common-prefix
---
## Q
**LC 14 最长公共前缀**｜Easy

返回字符串数组 `strs` 的最长公共前缀，没有则返回 `""`。

## A
**一句话。** 纵向扫描，`zip(*strs)` 按列取字符，某列不全相同就停。

```python
def longest_common_prefix(strs):
    size = 0
    for col in zip(*strs):       # 在最短串处自动停
        if len(set(col)) != 1:
            break
        size += 1
    return strs[0][:size]
```

**复杂度。** 时间 `O(S)`，空间 `O(n)`。

**易错点。**
- 以第一个串的长度为上界直接下标访问：`["flower","flow"]` 抛 `IndexError`，用 `zip` 避开。
- 只比前两个串：`["flower","flow","flight"]` 得 `"flow"`，应为 `"fl"`。

**追问。**
- 更短的写法？：只比字典序最小和最大的两个串。
- 查询频繁怎么办？：建 Trie，前缀是从根到第一个分叉或词尾的路径。

**同模式。** LC 208 实现 Trie、LC 1268 搜索推荐系统、LC 720 词典中最长的单词
