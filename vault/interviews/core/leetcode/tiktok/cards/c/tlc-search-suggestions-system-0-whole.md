---
id: tlc-search-suggestions-system-0-whole
node: c.search-suggestions-system
type: qa
---
## Q
**LC 1268 搜索推荐系统**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 2 次 · 最近 2023-03-09（国内 CodeTop）

给定字符串数组 `products` 和字符串 `searchWord`。依次输入 `searchWord` 的每个字母，每输入一个字母，推荐 `products` 中前缀与当前输入相同的最多三个产品；如果超过三个，按字典序返回最小的三个。返回二维列表，第 `i` 项是输入前 `i + 1` 个字母后的推荐。`1 <= products.length <= 1000`，`1 <= Σ products[i].length <= 2 * 10^4`，`1 <= searchWord.length <= 1000`，全部为小写字母。例：`products = ["mobile","mouse","moneypot","monitor","mousepad"]`，`searchWord = "mouse"` → `[["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先把 `products` 排序，匹配某前缀的产品在排序后是连续的一段，二分找到这段的起点，取最多三个。

**识别。** 「前缀匹配 + 字典序最小的前几个」：排序后，以某前缀开头的字符串恰好是一段连续区间，起点用 `bisect_left` 找；要不要建前缀树（Trie）取决于查询次数。

**推导。** 对每个前缀把全体产品筛一遍再排序：`O(L · n · l)`。洞察：排序只需一次；某前缀的所有匹配项在排序数组里紧挨着，且排在前面的就是字典序最小的，所以二分到起点后看后面三个是否仍以该前缀开头即可。输入越长，前缀越大，起点只会往右移，下一次二分可以从上一个起点开始。

**简单解法。** 同样先排序，但每个前缀线性扫描，不做二分。

```python
def suggested_products_scan(products: list[str], searchWord: str) -> list[list[str]]:
    products = sorted(products)
    return [
        [p for p in products if p.startswith(searchWord[:i])][:3]    # 排序后过滤，前三个即字典序最小的
        for i in range(1, len(searchWord) + 1)
    ]
```

`O(L · n · l)`，在 `n = 1000`、`L = 1000` 时约 `10^6` 次 `startswith`，可以通过；产品和查询再多就需要二分或 Trie。

最优解：

```python
from bisect import bisect_left


def suggested_products(products: list[str], searchWord: str) -> list[list[str]]:
    products = sorted(products)
    ans: list[list[str]] = []
    lo = 0                                       # 匹配区间的起点；前缀变长，起点只会不减
    for i in range(1, len(searchWord) + 1):
        prefix = searchWord[:i]
        lo = bisect_left(products, prefix, lo)   # 第一个 >= prefix 的位置
        # 区间里字典序最小的三个；不以 prefix 开头说明区间已结束
        ans.append([p for p in products[lo:lo + 3] if p.startswith(prefix)])
    return ans
```

运行：示例 1 得到题面给出的五组结果；`products = ["havana"]`，`searchWord = "tatiana"` → 七个 `[]`；`["bags","baggage","banner","box","cloths"]`，`"bags"` → `[["baggage","bags","banner"],["baggage","bags","banner"],["baggage","bags"],["bags"]]`。

**复杂度。** 排序 `O(S log n)`（`S` 为总字符数，比较成本摊进来），每个前缀一次二分 `O(l log n)`，总 `O(L · l · log n)`；空间 `O(S)`。

**拓展优化。**
- 查询次数很多、产品集合固定：建 Trie，每个节点预存字典序最小的三个产品，每次输入一个字母只走一步，`O(1)` 出结果。

```python
from typing import Any


def suggested_products_trie(products: list[str], searchWord: str) -> list[list[str]]:
    root: dict[str, Any] = {}
    for word in sorted(products):                # 按字典序插入，节点上的前三个就是最小的三个
        node = root
        for ch in word:
            node = node.setdefault(ch, {})
            top3 = node.setdefault("#", [])      # "#" 不是小写字母，不会和子节点冲突
            if len(top3) < 3:
                top3.append(word)
    ans: list[list[str]] = []
    node = root
    for ch in searchWord:
        node = node.get(ch, {})                  # 走丢后一直停在空节点，之后全部返回 []
        ans.append(node.get("#", []))
    return ans
```

- 产品持续增加、前缀要求带权重（热度）：节点上改存按热度排序的 top 3，插入时更新。

**易错点。**
- 忘了先排序：返回的是输入顺序的前三个，不是字典序最小的三个。
- 二分后不检查 `startswith`：`"mouse"` 的位置后面可能是 `"moustache"` 之类不匹配的词，必须过滤。
- 把 `bisect_left` 写成 `bisect_right`：恰好等于前缀的产品（如 `"bags"` 对前缀 `"bags"`）会被漏掉。

**追问。**
- 输入过程中可以退格：Trie 版本保存路径节点栈即可。
- 产品太多放不进内存：按首字母或分片的有序文件做二分，Trie 版本换成前缀分片的缓存。

**同模式。** LC 208 实现前缀树、LC 648 单词替换、LC 211 添加与搜索单词、LC 642 设计搜索自动补全系统、LC 14 最长公共前缀。
