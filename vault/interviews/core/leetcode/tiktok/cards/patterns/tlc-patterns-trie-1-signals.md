---
id: tlc-patterns-trie-1-signals
node: patterns.trie
type: qa
step: 1
---
## Q
**字典树（Trie）｜信号**

什么样的题面该想到字典树？它比哈希表多提供了什么能力？

## A
字典树（Trie，前缀树）把一组字符串按字符逐层存成一棵树：从根到某个节点的路径就是一个前缀；节点上有标记表示"这里是一个完整单词的结尾"。

**触发信号：**
- 反复查询"有没有以某串**开头**的单词"（前缀）：自动补全、`startsWith`（例：LC 1268 搜索推荐系统；高频：LC 208 实现 Trie (前缀树)）。
- 查询带**通配符**：`"b.."`、`".ad"`（LC 211）——哈希表无法处理，字典树可以在每层分叉（例：LC 211 添加与搜索单词 - 数据结构设计）。
- 在棋盘上**一次搜很多个单词**：LC 212。把单词放进字典树，沿着棋盘走的同时沿着树走，走不通立即剪枝（例：LC 212 单词搜索 II）。
- 多个字符串的**最长公共前缀**（LC 14）（高频：LC 3093 最长公共后缀查询）。
- 按路径分层的结构：文件系统 LC 588，每一层是一个目录名（例：LC 588 设计内存文件系统）。
- 数字的**二进制位**当作"字符"：每一层是一个比特，查询时每层优先走与当前位相反的分支，就能凑出最大异或。

**它比哈希表多的能力**：哈希表只回答"整个串在不在"，字典树能回答"有没有以它为前缀的串"，并且共享公共前缀以节省空间。

**复杂度**：插入、查询都是 `O(L)`（`L` 为串长），与单词总数无关；空间最坏 `O(所有字符总数)`。

**近似信号：**
- 只需判断整串是否存在 ⇒ `set`（例：LC 139 单词拆分）。
- 单词不多且只比较一次 ⇒ 排序后比较相邻即可（例：LC 14 最长公共前缀）。
- 要找子串（不一定从开头）⇒ 后缀树 / 滚动哈希 / KMP（例：LC 28 找出字符串中第一个匹配项的下标）。

**例题：** LC 1268 搜索推荐系统

产品数组 `products`（至多 1000 个）和 `searchWord`（长度至多 1000，均为小写字母）；`searchWord` 每输入一个字母，就从 `products` 中找出以当前前缀开头、字典序最小的至多三个产品。返回每一步的推荐列表。

```python
import bisect
def suggested_products(products: list[str], search_word: str) -> list[list[str]]:
    products.sort()
    lo, hi = 0, len(products)
    prefix = ""
    result: list[list[str]] = []
    for ch in search_word:
        prefix += ch
        lo = bisect.bisect_left(products, prefix, lo, hi)
        hi = bisect.bisect_left(products, prefix + chr(127), lo, hi)
        result.append(products[lo:min(lo + 3, hi)])
    return result
```

**例题：** LC 211 添加与搜索单词 - 数据结构设计

设计 `WordDictionary`：`addWord(word)` 添加单词，`search(word)` 判断是否有已添加的单词与 `word` 匹配，`word` 里的 `.` 可以匹配任意一个字母。单词长度 `1..25`，小写字母，最多调用 `10^4` 次。

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

**例题：** LC 212 单词搜索 II

`m x n` 小写字母网格（`1 <= m, n <= 12`）和单词列表 `words`（至多 `3 * 10^4` 个，每个长 `1..10`），返回所有能在网格中沿相邻单元格（不重复使用）拼出的单词。

```python
from typing import Any
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    root: dict[str, Any] = {}              # 字典树：字符 -> 子结点；'$' -> 在此结束的整词
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
        if word := node.pop('$', None):    # 取走整词：同一个词不会被找到两次
            found.append(word)
        board[i][j] = '#'                  # 占位，路径内不重复使用同一格
        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= ni < m and 0 <= nj < n and board[ni][nj] in node:
                dfs(ni, nj, node)
        board[i][j] = ch                   # 回溯
        if not node:                       # 这条分支的词都找完了：剪掉，之后不再进入
            del parent[ch]
    for i in range(m):
        for j in range(n):
            if board[i][j] in root:
                dfs(i, j, root)
    return found
```

**例题：** LC 588 设计内存文件系统

设计内存文件系统：`ls(path)` 列出目录内容（文件路径则只返回文件名，结果按字典序），`mkdir(path)` 逐级建目录，`addContentToFile(path, content)` 追加内容（文件不存在则创建），`readContentFromFile(path)` 读取内容。

```python
class _Entry:
    def __init__(self) -> None:
        self.children: dict[str, "_Entry"] = {}
        self.content: str | None = None    # None 表示目录，字符串表示文件
class FileSystem:
    def __init__(self) -> None:
        self.root = _Entry()
    def _walk(self, path: str, create: bool = False) -> _Entry:
        node = self.root
        for name in filter(None, path.split("/")):     # "/" 拆出来是 ["", ""]，filter 去掉空串
            if create:
                node = node.children.setdefault(name, _Entry())
            else:
                node = node.children[name]
        return node
    def ls(self, path: str) -> list[str]:
        node = self._walk(path)
        if node.content is not None:                   # 文件：只返回它自己的名字
            return [path.rsplit("/", 1)[-1]]
        return sorted(node.children)
    def mkdir(self, path: str) -> None:
        self._walk(path, create=True)
    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._walk(filePath, create=True)
        node.content = (node.content or "") + content  # 追加，不是覆盖
    def readContentFromFile(self, filePath: str) -> str:
        return self._walk(filePath).content or ""
```

**例题：** LC 139 单词拆分

字符串 `s`（`1 <= s.length <= 300`）和字典 `wordDict`（至多 1000 个词，每词长 `1..20`，词可重复使用），判断 `s` 能否拆成字典中的单词序列。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)                       # 哈希集合：判断"切片是不是单词"是 O(L)
    max_len = max(map(len, words))               # 单词最长 max_len，更长的切片不用试
    dp = [True] + [False] * len(s)               # dp[i]：前 i 个字符 s[:i] 能否被拆成单词
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(max(0, i - max_len), i))
    return dp[-1]
```

**例题：** LC 14 最长公共前缀

字符串数组 `strs`（`1 <= strs.length <= 200`，每个长 `0..200`，小写字母），求所有字符串的最长公共前缀，没有则返回 `""`。

```python
def longest_common_prefix(strs: list[str]) -> str:
    size = 0
    for column in zip(*strs):                    # 按列扫：第 j 列是所有字符串的第 j 个字符；zip 在最短串处自动停
        if len(set(column)) != 1:                # 这一列有不同字符：前缀到此为止
            break
        size += 1
    return strs[0][:size]
```

**例题：** LC 28 找出字符串中第一个匹配项的下标

给字符串 `haystack` 和 `needle`，返回 `needle` 在 `haystack` 中第一次出现的下标（从 0 开始），不存在就返回 `-1`。`1 <= haystack.length, needle.length <= 10^4`，两个字符串都只含小写英文字母。

```python
def str_str(haystack: str, needle: str) -> int:
    fail = [0] * len(needle)                   # fail[i]：needle[:i+1] 最长的「既是前缀又是后缀」的真前缀长度
    k = 0
    for i in range(1, len(needle)):
        while k and needle[i] != needle[k]:
            k = fail[k - 1]                    # 失配：退到次长的公共前后缀
        if needle[i] == needle[k]:
            k += 1
        fail[i] = k
    k = 0                                      # 当前已匹配 needle 的前 k 个字符
    for i, ch in enumerate(haystack):
        while k and ch != needle[k]:
            k = fail[k - 1]                    # haystack 的下标 i 永不回退
        if ch == needle[k]:
            k += 1
        if k == len(needle):
            return i - k + 1
    return -1
```

**例题：** LC 208 实现 Trie (前缀树)

实现前缀树（Trie）类：`Trie()` 初始化；`insert(word)` 插入单词；`search(word)` 若 `word` 已被插入返回 `true`，否则 `false`；`startsWith(prefix)` 若某个已插入单词以 `prefix` 为前缀返回 `true`。约束：`1 <= word.length, prefix.length <= 2000`，仅小写英文字母；三种操作总共调用不超过 `3 * 10^4` 次。

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

**例题：** LC 3093 最长公共后缀查询

给两个字符串数组 `wordsContainer` 和 `wordsQuery`。对每个 `wordsQuery[i]`，在 `wordsContainer` 中找一个与它有最长公共后缀的字符串；如果有多个，取长度最短的；长度也相同，取在 `wordsContainer` 中下标最小的。返回数组 `ans`，`ans[i]` 是对应的下标（没有任何公共后缀时，公共后缀是空串，所有容器字符串都满足，按同样的规则选）。`1 <= wordsContainer.length, wordsQuery.length <= 10^4`，`1 <= wordsContainer[i].length <= 5 * 10^3`，`1 <= wordsQuery[i].length <= 5 * 10^3`，字符串只含小写英文字母，`wordsContainer[i].length` 的总和和 `wordsQuery[i].length` 的总和都至多为 `5 * 10^5`。

```python
def string_indices(words_container: list[str], words_query: list[str]) -> list[int]:
    nxt: list[dict[str, int]] = [{}]    # 反向字典树：nxt[u][c] 是节点 u 的孩子
    best: list[int] = [0]               # best[u]：经过 u 的容器单词里，最短且最早的下标

    def better(i: int, j: int) -> int:  # 长度短者胜；等长时下标小者胜
        return i if (len(words_container[i]), i) < (len(words_container[j]), j) else j

    for idx, word in enumerate(words_container):
        best[0] = better(idx, best[0])  # 根节点代表空后缀：所有单词都经过
        u = 0
        for ch in reversed(word):       # 从最后一个字符往前插入
            if ch not in nxt[u]:
                nxt[u][ch] = len(nxt)
                nxt.append({})
                best.append(idx)
            u = nxt[u][ch]
            best[u] = better(idx, best[u])

    ans: list[int] = []
    for q in words_query:
        u = 0
        for ch in reversed(q):          # 沿查询词的反向尽量往深走
            if ch not in nxt[u]:
                break
            u = nxt[u][ch]
        ans.append(best[u])             # 停下的节点就是最长公共后缀对应的节点
    return ans
```
