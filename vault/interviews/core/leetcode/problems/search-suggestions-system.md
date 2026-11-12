---
slug: search-suggestions-system
---
## Q
**LC 1268 搜索推荐系统**｜Medium

逐个输入 `searchWord` 的字母，每次推荐 `products` 中与当前前缀匹配、字典序最小的至多三个产品。

## A
**一句话。** 先排序，匹配某前缀的产品在排序后连续，二分找起点取三个。

```python
def suggested_products(products, searchWord):
    products = sorted(products)
    ans = []
    lo = 0                     # 前缀变长，起点只会不减
    for i in range(1, len(searchWord) + 1):
        prefix = searchWord[:i]
        lo = bisect_left(products, prefix, lo)
        top = products[lo:lo + 3]
        ans.append([p for p in top if p.startswith(prefix)])
    return ans
```

**复杂度。** 时间 `O(S log n + L·l·log n)`，空间 `O(S)`。

**易错点。**
- 忘了先排序：得到输入顺序的前三个，不是字典序最小的。
- 二分后不检查 `startswith`：`["mouse","moustache"]` 前缀 `"mouse"` 会带上 `"moustache"`，应为 `["mouse"]`。
- 用 `bisect_right`：恰好等于前缀的产品会被漏掉。

**追问。**
- 输入过程中可以退格？：用 Trie，保存路径节点栈。

**同模式。** LC 208 实现 Trie (前缀树)、LC 648 单词替换、LC 642 设计搜索自动补全系统、LC 14 最长公共前缀
