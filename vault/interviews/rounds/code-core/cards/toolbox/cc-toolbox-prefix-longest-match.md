---
id: cc-toolbox-prefix-longest-match
node: toolbox.prefix-trees
type: qa
---
## Q
A routing table maps number prefixes to owners: `4242` → one brand, `424242` → a sub-brand. Which entry wins for `4242429999`, and how do you find it?

## A
**Longest-prefix match: walk the key one character at a time and remember the deepest node that carried a value.**

```python
best, node = None, root
for ch in key:
    node = node.get(ch)
    if node is None:
        break
    if "val" in node:
        best = node["val"]
```

- Remember as you go — not "walk to the end and back up". The key usually leaves the trie before the deepest match, and there is nothing to back up from.
- **Shortest**-prefix match is the same walk stopping at the first value. Specs mean one or the other; "any matching prefix" is never the rule.
- A key with no match at all returns the declared default, which is a sentinel decision ([[cc-output-sentinels-error-contract]]).
- With fixed-width numeric keys a sorted list plus one `bisect` does the same job; the trie version is what generalizes to wildcards and variable-length segments.

## Q zh
一张路由表把号码前缀映射到归属：`4242` → 某品牌，`424242` → 某子品牌。`4242429999` 命中哪一条，怎么找？

## A zh
**最长前缀匹配：逐字符沿 key 走，并记住最深的那个带值节点。**

```python
best, node = None, root
for ch in key:
    node = node.get(ch)
    if node is None:
        break
    if "val" in node:
        best = node["val"]
```

- 边走边记 —— 而不是「走到底再回溯」。key 通常在到达最深匹配之前就走出了 trie，那时根本无从回溯。
- **最短**前缀匹配是同样的走法，在第一个带值节点停下。spec 指的要么是这个要么是那个；「任意匹配的前缀」从来不是规则。
- 完全没有匹配的 key 返回约定的默认值，这是哨兵决定（[[cc-output-sentinels-error-contract]]）。
- 定宽数字 key 用有序列表加一次 `bisect` 也能做到同样的事；trie 版本的价值在于能推广到通配符和变长分段。
