---
id: uth-compose-http-router-2-radix-tree
node: compose.http-router
type: qa
step: 2
---
## Q
**方法表 + 基数树**｜httprouter · v1.3.0

httprouter 的路由表由哪几块结构拼成？它们怎样互相指向？

## A
**结构。** 外层一张表：HTTP 方法 → 这个方法自己的树根，每个方法各一棵基数树（radix tree，把公共前缀合并成一个节点的前缀树）。节点存一小段路径 `path`、孩子数组 `children`、各孩子首字节连成的字符串 `indices`、可选的处理函数 `handle`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="34" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">trees</text>
<rect x="8.0" y="28" width="52" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="34" y="44.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GET</text>
<rect x="8.0" y="58" width="52" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="34" y="74.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">POST</text>
<text x="34" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">方法 -&gt; 树根</text>
<rect x="173.0" y="28" width="34" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="190" y="44.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">/</text>
<line x1="60" y1="40" x2="165.0" y2="40.0" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="172,40 165.0,36.8 165.0,43.2" style="fill:var(--accent,#3b6fd4)"/>
<rect x="100.0" y="92" width="30" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="115" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">s</text>
<rect x="226.0" y="92" width="58" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="255" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">user/</text>
<line x1="180" y1="52" x2="120" y2="92" stroke="currentColor" stroke-width="1"/>
<line x1="200" y1="52" x2="250" y2="92" stroke="currentColor" stroke-width="1"/>
<text x="142" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s</text>
<text x="236" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">u</text>
<rect x="35.0" y="152" width="62" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="66" y="168.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">earch</text>
<rect x="116.0" y="152" width="68" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="150" y="168.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">upport</text>
<rect x="230.0" y="152" width="50" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="255" y="168.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">:id</text>
<rect x="230" y="152" width="50" height="24" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1.5" stroke-dasharray="4 3"/>
<line x1="105" y1="116" x2="75" y2="152" stroke="currentColor" stroke-width="1"/>
<line x1="125" y1="116" x2="142" y2="152" stroke="currentColor" stroke-width="1"/>
<line x1="255" y1="116" x2="255" y2="152" stroke="currentColor" stroke-width="1"/>
<text x="80" y="134" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">e</text>
<text x="144" y="134" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">u</text>
<rect x="12" y="196" width="22" height="14" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="40" y="207" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">有处理函数</text>
<rect x="120" y="196" width="22" height="14" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1.5" stroke-dasharray="4 3"/>
<text x="148" y="207" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">占位符节点</text>
<text x="170" y="226" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">GET /search  GET /support  GET /user/:id</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| 注册 | 方法表取（或建）树根，再沿公共前缀下行，必要时拆节点 | 随路径长度 |
| 查找 | 方法表取树根，逐层按首字节选孩子，遇到占位符节点就记下参数 | 随路径长度，每层扫一遍 `indices` |
| 方法没注册过 | 只查方法表 | O(1) |

**为什么。** 按方法分树，比在每个节点里放一张「方法 → 处理函数」的表省空间，也让查找开始前就砍掉一大片。

**例题：** LC 208 实现前缀树 Trie

实现前缀树 `Trie`：`insert(word)` 插入单词，`search(word)` 完整单词存在才为真，`startsWith(prefix)` 有单词以它开头就为真。只含小写字母，三种操作合计不超过 3·10^4 次。例：`insert("apple")` 后，`search("apple")` → `true`，`search("app")` → `false`，`startsWith("app")` → `true`。路由树去掉压缩和占位符，就是这棵前缀树。

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
