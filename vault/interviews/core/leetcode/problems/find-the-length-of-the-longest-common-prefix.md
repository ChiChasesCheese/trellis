---
slug: find-the-length-of-the-longest-common-prefix
---
## Q
**LC 3043 最长公共前缀的长度**｜Medium

给两个正整数数组，求 `arr1` 中某数与 `arr2` 中某数的最长公共前缀（按数字位数计）的长度，没有返回 `0`。

## A
**一句话。** 把 `arr1` 每个数的全部前缀放进集合，`arr2` 每个数逐位去掉末位，第一个命中的就是它的最长公共前缀。

```python
def longest_common_prefix(arr1, arr2):
    prefixes = set()
    for x in arr1:
        while x and x not in prefixes:   # 已在集合则更短前缀也在
            prefixes.add(x)
            x //= 10                     # 去掉末位 = 前一个前缀
    best = 0
    for y in arr2:
        while y and y not in prefixes:
            y //= 10
        if y:
            best = max(best, len(str(y)))
    return best
```

**复杂度。** 时间 `O((n+m)·9)`，空间 `O(n·9)`。

**易错点。**
- 只存 `arr1` 里完整的数：`[123]`、`[129]` 得 `0`，应为 `2`。
- 没判 `y` 非零就算位数：`len(str(0))` 是 `1`，把没有公共前缀算成长度 `1`。

**追问。**
- 字典树怎么做？：`arr1` 的数字串插入字典树，`arr2` 的数沿树走，最大深度即答案。
- 不用集合怎么做？：转成字符串合并排序，最长公共前缀出现在来自不同数组的相邻对之间。

**同模式。** LC 14 最长公共前缀、LC 208 实现 Trie (前缀树)、LC 1268 搜索推荐系统、LC 648 单词替换
