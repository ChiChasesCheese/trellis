---
id: tlc-implement-trie-prefix-tree-2-code
node: a.implement-trie-prefix-tree
type: qa
step: 2
---
## Q
**LC 208 实现 Trie (前缀树)**｜写出 Python 实现

实现 `Trie` 类，方法 `insert(word: str)`、`search(word: str) -> bool`、`startsWith(prefix: str) -> bool`。单词与前缀长度 `1..2000`，仅小写字母，操作总数 `<= 3·10^4`。每个操作应是 `O(L)`（`L` 为参数长度）。

## A
**思路。** 每个 `TrieNode` 有 `children`（字符到子结点的字典）和 `end`（是否有单词在此结束）。`insert` 沿字符往下走，缺哪个字符就建哪个结点，最后把终点的 `end` 置真。`_walk(s)` 沿 `s` 往下走，走不通返回 `None`，走到底返回终点结点。`search` 要求终点存在且 `end` 为真，`startsWith` 只要求终点存在。

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

**写法要点。** `__slots__` 去掉每个结点的 `__dict__`，结点多时明显省内存；子结点用 `dict[str, TrieNode]` 而不是长度 26 的列表，只为实际出现的字符付空间，字符集换成 Unicode 也不用改；`_walk` 里的海象运算符 `(node := node.children.get(ch)) is None` 把「取子结点」和「判空」合成一行；把 `search` 和 `startsWith` 的共同部分提取成 `_walk`，两者只差一次 `end` 判断；`insert` 用 `if ch not in ...` 而不是 `setdefault(ch, TrieNode())`，后者每步都会白造一个结点。
