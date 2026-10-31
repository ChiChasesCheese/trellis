---
id: tlc-patterns-trie-9-problems
node: patterns.trie
type: qa
step: 9
---
## Q
**字典树（Trie）｜本组用到字典树的题**

按变形分类，这个题组里哪些题属于字典树？

## A
- 基础与通配符：LC 211 添加与搜索单词、LC 208 实现 Trie (前缀树)（高频）
- 网格 + 回溯：LC 212 单词搜索 II
- 前缀：LC 14 最长公共前缀、LC 3093 最长公共后缀查询（高频）
- 路径树：LC 588 设计内存文件系统
- 与 DP 搭配：LC 139 单词拆分、LC 140 单词拆分 II（词典可用字典树加速前缀匹配）

提示：先问"是整串查询还是前缀查询、有没有通配符、是不是要同时搜很多单词"；是前缀或通配符就用字典树。

**例题：** LC 211 添加与搜索单词

实现 `WordDictionary`：`addWord(word)` 添加小写单词，`search(word)` 判断是否存在匹配的单词，其中 `'.'` 可以匹配任意一个字母；单词长度 `<= 25`，至多调用 `10^4` 次。

```python
class WordDictionary:
    def __init__(self) -> None:
        self.root: dict[str, dict] = {}
    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = {}
    def search(self, word: str) -> bool:
        def dfs(node: dict[str, dict], i: int) -> bool:
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)
```

**例题：** LC 212 单词搜索 II

给 `m x n` 的字符网格（`m, n <= 12`）和单词列表 `words`（最多 `3 * 10^4` 个，每个长度 `<= 10`），返回所有能在网格里按相邻格拼出的单词，同一格在一个单词里不能重复使用。

```python
from typing import Any
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    root: dict[str, Any] = {}
    for word in words:
        node = root
        for ch in word:
            node = node.setdefault(ch, {})
        node['$'] = word
    m, n = len(board), len(board[0])
    found: list[str] = []
    def dfs(i: int, j: int, parent: dict[str, Any]) -> None:
        ch = board[i][j]
        node = parent[ch]
        if word := node.pop('$', None):
            found.append(word)
        board[i][j] = '#'
        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= ni < m and 0 <= nj < n and board[ni][nj] in node:
                dfs(ni, nj, node)
        board[i][j] = ch
        if not node:
            del parent[ch]
    for i in range(m):
        for j in range(n):
            if board[i][j] in root:
                dfs(i, j, root)
    return found
```

**例题：** LC 14 最长公共前缀

给字符串数组 `strs`（`<= 200` 个，每个长度 `<= 200`），返回它们的最长公共前缀，没有则返回 `""`。

```python
def longest_common_prefix(strs: list[str]) -> str:
    size = 0
    for column in zip(*strs):
        if len(set(column)) != 1:
            break
        size += 1
    return strs[0][:size]
```

**例题：** LC 588 设计内存文件系统

实现 `FileSystem`：`ls(path)`、`mkdir(path)`（缺失的中间目录一并创建）、`addContentToFile(filePath, content)`（追加内容，文件不存在则创建）、`readContentFromFile(filePath)`；路径为绝对路径，至多调用 `300` 次。

```python
class _Entry:
    def __init__(self) -> None:
        self.children: dict[str, "_Entry"] = {}
        self.content: str | None = None
class FileSystem:
    def __init__(self) -> None:
        self.root = _Entry()
    def _walk(self, path: str, create: bool = False) -> _Entry:
        node = self.root
        for name in filter(None, path.split("/")):
            if create:
                node = node.children.setdefault(name, _Entry())
            else:
                node = node.children[name]
        return node
    def ls(self, path: str) -> list[str]:
        node = self._walk(path)
        if node.content is not None:
            return [path.rsplit("/", 1)[-1]]
        return sorted(node.children)
    def mkdir(self, path: str) -> None:
        self._walk(path, create=True)
    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._walk(filePath, create=True)
        node.content = (node.content or "") + content
    def readContentFromFile(self, filePath: str) -> str:
        return self._walk(filePath).content or ""
```

**例题：** LC 139 单词拆分

给字符串 `s`（长度 `<= 300`）和字典 `wordDict`，判断 `s` 能否拆成一个或多个字典单词（单词可重复使用）。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)
    max_len = max(map(len, words))
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(max(0, i - max_len), i))
    return dp[-1]
```

**例题：** LC 140 单词拆分 II

给字符串 `s`（`s.length <= 20`）和字典 `wordDict`，在 `s` 中插入空格组成句子，使每个单词都在字典里（可重复使用），返回所有这样的句子。

```python
from functools import cache
def word_break(s: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)
    max_len = max(map(len, words))
    @cache
    def sentences(i: int) -> tuple[str, ...]:
        if i == len(s):
            return ('',)
        found: list[str] = []
        for j in range(i + 1, min(len(s), i + max_len) + 1):
            if (word := s[i:j]) in words:
                for rest in sentences(j):
                    found.append(f'{word} {rest}' if rest else word)
        return tuple(found)
    return list(sentences(0))
```

**例题：** LC 208 实现 Trie (前缀树)

实现 `Trie`：`insert(word)` 插入，`search(word)` 判断整词是否存在，`startsWith(prefix)` 判断是否有以 `prefix` 开头的词；长度 `<= 2000`，总调用 `<= 3 * 10^4`。

```python
class TrieNode:
    __slots__ = ("children", "end")
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.end = False
class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()
    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True
    def _walk(self, s: str) -> TrieNode | None:
        node = self.root
        for ch in s:
            if (node := node.children.get(ch)) is None:
                return None
        return node
    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.end
    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
```

**例题：** LC 3093 最长公共后缀查询

对每个 `wordsQuery[i]`，在 `wordsContainer` 里找与它公共后缀最长的字符串，并列取更短的，再并列取下标小的，返回下标数组；两个数组的总长度都 `<= 5 * 10^5`。

```python
def string_indices(words_container: list[str], words_query: list[str]) -> list[int]:
    nxt: list[dict[str, int]] = [{}]
    best: list[int] = [0]
    def better(i: int, j: int) -> int:
        return i if (len(words_container[i]), i) < (len(words_container[j]), j) else j
    for idx, word in enumerate(words_container):
        best[0] = better(idx, best[0])
        u = 0
        for ch in reversed(word):
            if ch not in nxt[u]:
                nxt[u][ch] = len(nxt)
                nxt.append({})
                best.append(idx)
            u = nxt[u][ch]
            best[u] = better(idx, best[u])
    ans: list[int] = []
    for q in words_query:
        u = 0
        for ch in reversed(q):
            if ch not in nxt[u]:
                break
            u = nxt[u][ch]
        ans.append(best[u])
    return ans
```
