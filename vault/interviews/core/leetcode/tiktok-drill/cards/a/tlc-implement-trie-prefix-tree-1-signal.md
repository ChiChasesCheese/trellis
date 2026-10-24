---
id: tlc-implement-trie-prefix-tree-1-signal
node: a.implement-trie-prefix-tree
type: qa
step: 1
---
## Q
**LC 208 实现 Trie (前缀树)**｜Medium · 字节 高频

实现前缀树（Trie）类：`Trie()` 初始化；`insert(word)` 插入单词；`search(word)` 若 `word` 已被插入返回 `true`，否则 `false`；`startsWith(prefix)` 若某个已插入单词以 `prefix` 为前缀返回 `true`。

约束：`1 <= word.length, prefix.length <= 2000`，仅小写英文字母；三种操作总共调用不超过 `3 * 10^4` 次。

例：`insert("apple")` 后，`search("apple")` → `true`，`search("app")` → `false`，`startsWith("app")` → `true`；再 `insert("app")`，`search("app")` → `true`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「前缀」出现在接口里（`startsWith`）→ 要在 `O(L)` 内回答前缀问题，集合 / 哈希表做不到（只会精确匹配）→ **前缀树**。
- 「很多字符串共享前缀」「自动补全 / 拼写检查」→ 公共前缀共用路径，省空间也省时间。
- 约束：单词长度到 `2000`、操作 `3·10^4` → 每个操作必须与单词总数无关，只和参数长度 `L` 成正比；存「所有前缀」的集合要 `O(L^2)` 空间，不可取。

**推导链。**
1. 暴力：集合存单词，`startsWith` 遍历所有单词用 `startswith` 检查，`O(N·L)`。
2. 改进：把每个单词的所有前缀也放进集合，`startsWith` 变 `O(L)`，但空间 `O(Σ L^2)`。
3. 洞察：前缀大量重叠，把重叠部分合并成树；再用 `end` 标记区分「路径存在」和「单词结束」。
4. 最优：每个结点一张 `dict[str, TrieNode]` + 一个 `end` 布尔；`insert` / `search` / `startsWith` 都是沿字符走 `O(L)`，空间 `O(总字符数)`。

**同模式的题**：LC 211 添加与搜索单词、LC 212 单词搜索 II、LC 648 单词替换、LC 1268 搜索推荐系统、LC 421 数组中两个数的最大异或。
