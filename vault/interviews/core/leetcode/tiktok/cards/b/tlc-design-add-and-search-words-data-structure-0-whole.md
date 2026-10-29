---
id: tlc-design-add-and-search-words-data-structure-0-whole
node: b.design-add-and-search-words-data-structure
type: qa
---
## Q
**LC 211 添加与搜索单词 - 数据结构设计**｜Medium · LC TikTok 热度 56/100 · CodeTop 国内累计 2 次 · 最近 2022-09-21（CodeTop）

设计一个数据结构，支持添加新单词，以及查找字符串是否与任何先前添加的单词匹配。实现 `WordDictionary` 类：`WordDictionary()` 初始化；`addWord(word)` 把 `word` 加入数据结构；`search(word)` 若存在与 `word` 匹配的字符串则返回 `true`，否则 `false`，其中 `word` 里的 `'.'` 可以表示任意一个字母。`1 <= word.length <= 25`；`addWord` 的 `word` 由小写字母组成；`search` 的 `word` 由 `'.'` 或小写字母组成；`addWord` 与 `search` 合计最多调用 `10^4` 次。例：依次 `addWord("bad")`、`addWord("dad")`、`addWord("mad")`，`search("pad")` → `false`，`search("bad")` → `true`，`search(".ad")` → `true`，`search("b..")` → `true`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用字典树（Trie）存单词：`addWord` 沿字母向下建结点，末尾打结束标记；`search` 逐字符向下走，遇到 `'.'` 就对所有孩子分支递归（DFS），走完全部字符后检查当前结点有没有结束标记。添加 `O(L)`，搜索最坏遍历整棵树。

**识别。** 「逐字符匹配 + 通配符」是字典树加回溯的信号。没有通配符时一个 `set` 就够；通配符让匹配在每个 `'.'` 处分叉，而字典树把共享前缀合并，分叉只在存在的孩子上展开，不会枚举 26 个字母的全部组合。单词长度不超过 `25`，递归深度安全。

**推导。** 暴力：列表存所有单词，`search` 时逐个比较，`O(N·L)`；浪费：不同单词的相同前缀被反复比较。洞察：字典树合并前缀；`'.'` 等价于「任选一个孩子」，对每个孩子递归，任一分支成功即成功。结束标记必须单独存，否则前缀会被当成单词。

```python
class WordDictionary:
    def __init__(self) -> None:
        self.root: dict[str, dict] = {}           # 字典树：键是字母，值是子结点；键 "$" 标记单词在此结束

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})        # 有就取、没有就建，一步完成
        node["$"] = {}

    def search(self, word: str) -> bool:
        def dfs(node: dict[str, dict], i: int) -> bool:
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":                         # 通配符：除结束标记外，每个孩子都试一遍
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)

        return dfs(self.root, 0)
```

**运行。** 加入 `bad`、`dad`、`mad` 后：`search("pad")` → `False`，`search("bad")` → `True`，`search(".ad")` → `True`，`search("b..")` → `True`；另有 `search("b")` → `False`，`search("badd")` → `False`，`search("....")` → `False`，`search("...")` → `True`。一万个长度 25 的随机单词，搜索 `"." * 25` 约 0.03 秒。

**复杂度。** `addWord` 时间 `O(L)`；`search` 无通配符时 `O(L)`，有通配符时最坏访问整棵树的所有结点，`O(总字符数)`；空间 `O(总字符数)`。

**易错点。**
- 没有结束标记，只靠路径存在：加入 `bad` 后，`search("b")` 和 `search("ba")` 都会返回 `True`，正确是 `False`，前缀不是单词。
- `'.'` 不能匹配"空"：它恰好消耗一个字符，所以 `search("...")` 的长度要与单词一致，`search("badd")` 在 `bad` 的结尾后没有孩子可走，返回 `False`。
- 结束标记 `"$"` 和字母放在同一个字典里，通配符展开时要排除这个键；用一个不会出现在单词里的符号。

**追问。**
- 支持 `*` 匹配任意长度（类似正则，LC 10）：不能再单纯 DFS，需要动态规划或带记忆的回溯。
- 单词删除：递归到末尾去掉结束标记，回溯时把没有孩子的结点从父结点里删掉。
- 通配符特别多、单词特别多：把 DFS 换成按层推进的结点集合（每遇到字母或 `.` 就推进一层），避免递归开销；或按长度分桶，先过滤出同长度的单词。

**同模式。** LC 208 实现 Trie、LC 212 单词搜索 II、LC 648 单词替换、LC 677 键值映射、LC 14 最长公共前缀。
