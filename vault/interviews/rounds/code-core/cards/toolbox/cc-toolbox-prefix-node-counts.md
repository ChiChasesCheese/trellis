---
id: cc-toolbox-prefix-node-counts
node: toolbox.prefix-trees
type: qa
---
## Q
"How many registered ids start with `p`" must answer in O(len(p)) while ids are still being inserted. What do you store?

## A
**An aggregate in every node, updated on the way down at insert time.**

```python
for ch in word:
    node = node.setdefault(ch, {"n": 0})
    node["n"] += 1
```

- The answer for `p` is the `n` at the node you land on — no subtree walk, no re-count.
- Any **associative** aggregate works the same way: count, sum, max, min, or a bitmask of which categories appear. Non-associative ones (median, distinct count) do not.
- Deletion decrements along the same path; a node whose count reaches 0 must be pruned, or it will still report the prefix as existing.
- This is precisely what a sorted list plus `bisect` cannot do cheaply once the set changes ([[cc-toolbox-prefix-sorted-bisect]]).

## Q zh
在 id 还在持续插入的同时，「有多少注册 id 以 `p` 开头」必须在 O(len(p)) 内回答。存什么？

## A zh
**在每个节点上存一个聚合量，插入时沿路径向下更新。**

```python
for ch in word:
    node = node.setdefault(ch, {"n": 0})
    node["n"] += 1
```

- `p` 的答案就是你走到的那个节点上的 `n` —— 不用遍历子树，不用重新计数。
- 任何**可结合**的聚合量都一样：计数、求和、最大、最小，或表示出现过哪些类别的位掩码。不可结合的（中位数、去重计数）不行。
- 删除时沿同一路径递减；计数归零的节点必须剪掉，否则它仍会把该前缀报告为存在。
- 这恰恰是有序列表加 `bisect` 在集合会变时做不到的（[[cc-toolbox-prefix-sorted-bisect]]）。
