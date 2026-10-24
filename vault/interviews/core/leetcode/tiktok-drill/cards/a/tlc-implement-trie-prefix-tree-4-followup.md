---
id: tlc-implement-trie-prefix-tree-4-followup
node: a.implement-trie-prefix-tree
type: qa
step: 4
---
## Q
**LC 208 实现 Trie (前缀树)**｜追问

面试官接着问：（1）支持 `delete(word)`？（2）`startsWith` 之外，要返回所有以 `prefix` 开头的单词（自动补全）？（3）单词里有通配符 `.`（LC 211）？

## A
1. **删除**：先确认单词存在；把终点 `end` 置假；若终点没有孩子，就沿路径往回删掉不再被其他单词使用的结点。迭代版需要一个 `(父结点, 字符)` 的路径栈；递归版在返回时判断「孩子为空且 `end` 为假」。
2. **自动补全**：`node = self._walk(prefix)` 之后，从 `node` 做 DFS，拼接路径上的字符，遇到 `end` 就收集。要返回频率最高的 `k` 个，可以在 `end` 结点存计数，并在每个结点缓存 top-k，写入时更新。
3. **通配符 `.`**：`search` 改成递归 / 栈：遇到普通字符走对应孩子，遇到 `.` 对所有孩子分叉。用栈 `[(node, i)]` 迭代，避免 2000 层递归。最坏要遍历整棵子树，复杂度和已存结点数相关。

**Python 提醒**：`dict.get(ch)` 返回 `None` 表示没有该孩子，与 `children[ch]` 的 `KeyError` 相比不用 `try`；而 `defaultdict(TrieNode)` 会在**读取**时创建键，把查询变成修改，Trie 的查询方法里不要用。
