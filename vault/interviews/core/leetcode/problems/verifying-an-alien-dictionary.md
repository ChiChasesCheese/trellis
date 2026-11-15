---
slug: verifying-an-alien-dictionary
---
## Q
**LC 953 验证外星语词典**｜Easy

外星语使用小写字母，但字母表顺序是给定的 `order`。给一组单词，判断它们是否按该语言的字典序排列。

## A
**一句话。** 把每个单词换成「字母在外星字母表里的名次」的列表，用列表比较（前缀较短者小）检查相邻是否不降。

```python
def is_alien_sorted(words, order):
    rank = {c: i for i, c in enumerate(order)}
    keys = [[rank[c] for c in w] for w in words]   # 换成名次列表
    return all(a <= b for a, b in pairwise(keys))  # 列表按字典序比
```

**复杂度。** 时间 `O(L)`，空间 `O(L)`（`L` 为字符总数）。

**易错点。**
- 只比第一个字符：首字母相同时要比后面的字符。
- 前缀关系：`"apple"` 排在 `"app"` 之前不合法，列表比较里较短的前缀更小，自动处理。

**追问。**
- 只检查相邻就够吗？：字典序是全序、传递，相邻不降则整体有序。
- 如果要推出字母表顺序（LC 269）？：相邻两词第一个不同的字符给出一条边，对字符图做拓扑排序。

**同模式。** LC 269 火星词典、LC 1086 前五科的均分
