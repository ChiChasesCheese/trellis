---
id: tlc-design-add-and-search-words-data-structure-2-code
node: b.design-add-and-search-words-data-structure
type: qa
step: 2
---
## Q
**LC 211 添加与搜索单词 - 数据结构设计**｜写出 Python 实现

实现 `WordDictionary` 类：`addWord(word)` 添加由小写字母组成的单词（长度 `1..25`）；`search(word)` 判断是否有已添加的单词与 `word` 匹配，`word` 由小写字母和 `'.'` 组成，`'.'` 可以表示任意一个字母。合计最多 `10^4` 次调用。

## A
**思路。** 字典树用嵌套 `dict` 表示：键是字母，值是子结点，键 `"$"` 表示一个单词在此结束。`addWord` 沿字母用 `setdefault` 建路径，末尾放 `"$"`。`search` 用内部递归 `dfs(node, i)`：到末尾看有没有 `"$"`；遇到 `'.'` 对所有字母孩子尝试；否则沿对应字母走。

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

**运行。** 加入 `bad`、`dad`、`mad`：`search("pad")` → `False`，`search("bad")` → `True`，`search(".ad")` → `True`，`search("b..")` → `True`；`search("b")` → `False`，`search("badd")` → `False`，`search("...")` → `True`。

**复杂度。** `addWord` 时间 `O(L)`；`search` 无通配符 `O(L)`，有通配符最坏访问整棵树，`O(总字符数)`；空间 `O(总字符数)`。

**写法要点。** `dict.setdefault(ch, {})` 把"取或建"压成一行；嵌套 `dict` 作字典树比定义结点类更短，稀疏分支也比 26 格数组省内存；`"$"` 键兼作结束标记；`any(生成器)` 在第一个成功的分支处短路；`ch in node and dfs(...)` 利用 `and` 的短路，字母不存在时直接返回 `False`；内部函数 `dfs` 访问外层的 `word`，不必每层传递。
