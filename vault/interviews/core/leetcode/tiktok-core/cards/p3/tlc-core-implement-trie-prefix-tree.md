---
id: tlc-core-implement-trie-prefix-tree
node: p3.implement-trie-prefix-tree
type: qa
---
## Q
**LC 208 实现 Trie (前缀树)**｜Medium · 近一年被问：美国 0 次、国内 3 次 · CodeTop 国内累计 18 次 · 最近 2026-10（国内面试记录） · 也在：LeetCode Hot 100、Blind 75、NeetCode 150、Top Interview 150

实现前缀树（Trie）类：`Trie()` 初始化；`insert(word)` 插入单词；`search(word)` 若 `word` 已被插入返回 `true`，否则 `false`；`startsWith(prefix)` 若某个已插入单词以 `prefix` 为前缀返回 `true`。

约束：`1 <= word.length, prefix.length <= 2000`，仅小写英文字母；三种操作总共调用不超过 `3 * 10^4` 次。

例：`insert("apple")` 后，`search("apple")` → `true`，`search("app")` → `false`，`startsWith("app")` → `true`；再 `insert("app")`，`search("app")` → `true`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** Trie 是一棵「每条边一个字符」的树：从根沿着单词的字符往下走，公共前缀共用同一段路径；结点上加一个 `end` 标记「有单词在此结束」，`search` 要求路径存在且 `end` 为真，`startsWith` 只要求路径存在。三个操作都是 `O(L)`。

**识别。** 「按前缀查询」「自动补全」「很多字符串共享前缀」是前缀树的信号；对比哈希集合：`search` 同样 `O(L)`，但 `startsWith` 要么 `O(总字符数)` 扫描，要么把每个单词的所有前缀都存一遍（`O(L^2)` 空间）。设计题还有一层考点：把「路径存在」和「单词结尾」分开。

**推导。** 朴素：用集合存单词，`search` 是 `O(L)`，`startsWith` 要遍历所有单词判断 `startswith`，`O(N·L)`。改进：把每个单词的所有前缀都放进另一个集合，`startsWith` 变 `O(L)`，但空间是 `O(Σ L^2)`（长度 2000 的单词要存 2000 个前缀，约 200 万字符）。浪费在于前缀之间大量重叠：`app` 是 `apple` 的前缀，却被存了两份。洞察：让重叠的部分共用结构——一棵树，沿着字符往下走，单词的前缀就是树上一条路径。再给结点打一个结尾标记以区分「`app` 只是前缀」和「`app` 是单词」。空间降到 `O(总字符数)`。

```python
class TrieNode:
    __slots__ = ("children", "end")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}   # 字符 -> 子结点
        self.end = False                          # 是否有单词恰好在这里结束


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:           # 不用 setdefault：它每次都会白造一个结点
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True

    def _walk(self, s: str) -> TrieNode | None:
        node = self.root
        for ch in s:
            if (node := node.children.get(ch)) is None:
                return None                       # 路走不通：没有以 s 为前缀的单词
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.end      # 路径存在还不够，必须是单词结尾

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
```

运行：`["Trie","insert","search","search","startsWith","insert","search"]` → `[None, None, True, False, True, None, True]`，`空 Trie 上 search / startsWith` → `[None, False, False]`，`insert("a") 后 search("ab") / startsWith("ab")` → `[None, None, False, False]`。

**复杂度。** 三个操作时间都是 `O(L)`（`L` 为单词或前缀长度，与已存单词数无关）；空间 `O(总字符数)`，最坏所有单词没有公共前缀，每个字符一个结点。

**易错点。**
- `search` 只检查路径存在、不看结尾标记：插入 `"apple"` 后 `search("app")` 错返回 `true`（正确 `false`）。
- `insert` 里用 `node.children.setdefault(ch, TrieNode())`：结果对，但每个字符都会无条件新造一个 `TrieNode` 再丢弃，大输入下白白拖慢。
- 用 `defaultdict` 自动建结点：`search` / `startsWith` 的查询也会悄悄创建结点，污染树，空树上 `startsWith("zzz")` 的这次查询本身就会造出 `z→z→z`，之后 `startsWith("zz")` 错返回 `true`。
- 结尾标记放错位置：标在最后一个字符的**边**上，或忘了在 `insert("app")` 时给已存在的 `p` 结点补标记。

**追问。**
- 再支持 `delete(word)`：先 `search` 确认存在，清掉 `end`；若该结点没有孩子，就沿路径回退删掉无用结点（需要记录路径栈）。
- 自动补全（返回所有以 `prefix` 开头的单词，或频率最高的 `k` 个）：`_walk(prefix)` 之后从该结点 DFS 收集；要按频率则每个结点缓存 top-k，或在 `end` 结点存计数。
- 含通配符 `.` 的查询（LC 211）：遇到 `.` 就对所有孩子递归；字符集只有 26 个，最坏 `O(26^L)` 但被已有结点数限制。

**同模式。** LC 211 添加与搜索单词、LC 212 单词搜索 II、LC 648 单词替换、LC 677 键值映射、LC 1268 搜索推荐系统、LC 421 数组中两个数的最大异或（二进制 Trie）。
