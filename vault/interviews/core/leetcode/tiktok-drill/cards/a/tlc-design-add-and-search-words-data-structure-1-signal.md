---
id: tlc-design-add-and-search-words-data-structure-1-signal
node: a.design-add-and-search-words-data-structure
type: qa
step: 1
---
## Q
**LC 211 添加与搜索单词 - 数据结构设计**｜Medium · LC TikTok 热度 56/100 · CodeTop 国内累计 2 次 · 最近 2022-09-21（CodeTop）

设计 `WordDictionary`：`addWord(word)` 添加单词；`search(word)` 判断是否存在与 `word` 匹配的已添加单词，其中 `word` 里的 `'.'` 可以匹配任意一个字母。

约束：`1 <= word.length <= 25`；`addWord` 的单词由小写字母组成；`search` 的词由 `'.'` 或小写字母组成；两类操作合计最多 `10^4` 次。例：加入 `bad`、`dad`、`mad` 后，`search("pad")` → `false`，`search(".ad")` → `true`，`search("b..")` → `true`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「逐字符匹配 + 单词集合」→ 字典树（Trie）：共享前缀，逐字符向下走。
- 「`'.'` 匹配任意一个字母」→ 在这一位分叉，对所有存在的孩子递归（DFS + 回溯）；任一分支成功即成功。
- 「设计类」题 → 先说数据结构（结点是什么、结束标记放哪里），再逐个方法说复杂度。
- 长度 `<= 25`、调用 `<= 10^4` 次 → 递归深度和总工作量都很小，不需要更复杂的结构。

**推导链。**
1. 暴力：列表保存所有单词，`search` 时对每个同长度的单词逐字符比较，`O(N·L)`。
2. 浪费：许多单词共享前缀，比较被重复。
3. 洞察：字典树把前缀合并；普通字母只走一条边，`'.'` 才分叉；结束标记单独存，避免把前缀当单词。
4. 最优：`addWord` `O(L)`，`search` 在无通配符时 `O(L)`，有通配符时最坏遍历整棵树。

**同模式的题**：LC 208 实现 Trie、LC 212 单词搜索 II、LC 648 单词替换、LC 677 键值映射。
