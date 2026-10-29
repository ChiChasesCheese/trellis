---
id: uth-os-net-page-cache-1-xarray
node: os-net.page-cache
type: qa
step: 1
---
## Q
**读文件为什么第二次很快**｜Linux · 页缓存 · 内核 7.3

一个文件的页缓存在内核里怎么存？按偏移找某一页是什么复杂度？

## A
**背景。** 第一次读文件要等磁盘；读过的数据内核会留在内存里（页缓存，page cache），下次直接从内存拷。接着有个查找问题：给定“文件的第 70 页”，怎样很快找到它在内存里的位置？哈希表可以，但页号是 0、1、2……稠密连续的整数，更适合一棵按位取下标的树。

**结构。** 每个文件（inode）有一个 `address_space`，它的 `i_pages` 是一棵 XArray：每个节点 64 个槽，每层取页号的 6 位当下标。例：页号 70 = 1×64 + 6，根节点取下标 1，下一层取下标 6，就找到了。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 188">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">页号 70 = 1 和 6 每层取 6 位</text>
<rect x="100" y="30" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="122" y="30" width="22" height="22" rx="1" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="133" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="144" y="30" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="166" y="30" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="188" y="30" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="210" y="30" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="232" y="30" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="254" y="30" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="46" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">64 槽</text>
<line x1="133" y1="54" x2="133" y2="81" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M133.0,86.0 L129.7,79.2 L136.3,79.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="45" y="90" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="67" y="90" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="89" y="90" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="111" y="90" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="133" y="90" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="155" y="90" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="177" y="90" width="22" height="22" rx="1" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="188" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">6</text>
<rect x="199" y="90" width="22" height="22" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="228" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">64 槽</text>
<line x1="188" y1="114" x2="188" y2="139" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M188.0,144.0 L184.7,137.2 L191.3,137.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="146" y="148" width="84" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="188" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">页 70</text>
</svg>
```

**细节。**

- XArray 是基数树（radix tree，按下标逐层分叉的树）的继任者；每层 6 位（`XA_CHUNK_SHIFT`），深度约 log64(页数)
- 查找可以用 RCU（读的时候不加锁的并发技巧）免锁
- `read()` 先查这棵树，命中就从内存拷贝，不碰磁盘

**为什么。** 页号稠密且连续，比哈希表省内存，还能高效取“下一页”，预读（提前把后面的页读进来）用得上。

**例题：** LC 208 实现 Trie（前缀树）（同类：LC 211 添加与搜索单词）

实现前缀树 `Trie`：`insert(word)` 插入单词，`search(word)` 判断完整单词是否存在，`startsWith(prefix)` 判断是否有单词以它为前缀。例：`insert("apple")` 后 `search("apple")` → `true`，`search("app")` → `false`，`startsWith("app")` → `true`。

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
