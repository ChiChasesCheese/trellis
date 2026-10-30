---
id: tlc-implement-trie-prefix-tree-3-why
node: p3.implement-trie-prefix-tree
type: qa
step: 3
---
## Q
**LC 208 实现 Trie (前缀树)**｜正确性

`search` 和 `startsWith` 为什么在同一条「走路径」的逻辑上只差一个 `end` 判断？如果没有 `end` 标记，会错在哪里？

## A
**不变量。** 从根沿字符串 `s` 的字符能走到的结点，当且仅当存在某个已插入单词以 `s` 为前缀；该结点的 `end` 为真，当且仅当 `s` 本身被插入过。

**为什么保持。** `insert(w)` 沿 `w` 的每个字符建出（或复用）一条路径，所以 `w` 的每个前缀都能走到；只有终点的 `end` 被置真，所以中间结点（更短的前缀）不会被误认为单词。

**所以。** `startsWith(p)` = 路径能走通；`search(w)` = 路径能走通**且**终点 `end` 为真。

**反例（没有 `end`）。** 先 `insert("apple")`，再 `search("app")`。路径 `a→p→p` 存在，没有标记的版本返回 `true`；带标记的版本发现终点 `p` 的 `end` 是假，返回 `false`。随后 `insert("app")` 把这个结点的 `end` 置真，`search("app")` 才变成 `true`——题目示例的 `[…, false, …, true]` 正是考这一点。
