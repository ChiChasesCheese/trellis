---
id: uth-storage-inverted-index-3-term-dict
node: storage.inverted-index
type: qa
step: 3
---
## Q
**词典：从 FST 到前缀树**｜Lucene · 10.5

几千万个词怎么快速查到它的列表位置？Lucene 的词典索引不只是个排序数组吗？

## A
**背景。** 查一个词的文档号列表之前，先要在词典里找到这个词。排序数组要二分、比较整个词；哈希表快，却没有顺序，没法查“以 ti 开头的所有词”。

**结构。** 词典分块存在 `.tim`（默认每块 25–48 个词），索引 `.tip` 只记各块的前缀。Lucene 10.2 及之前，这个索引是 FST（有限状态转换器，finite state transducer）：把共享前缀、后缀的词压成一个自动机，沿着边走到终点，输出块的文件位置；10.3 起换成专用的前缀树（trie，沿字符一层层往下走的树）。下图是前缀树的样子：查 tip 沿 t、i、p 走三步。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 188">
<line x1="162.1" y1="26.3" x2="100.5" y2="60.2" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="177.9" y1="26.3" x2="239.5" y2="60.2" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="90" y1="78" x2="90" y2="98" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="241.9" y1="74.9" x2="218.1" y2="101.1" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="258.1" y1="74.9" x2="281.9" y2="101.1" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="204.3" y1="120.5" x2="191.7" y2="143.5" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="215.7" y1="120.5" x2="228.3" y2="143.5" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="290" y1="122" x2="290" y2="142" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<circle cx="170" cy="22" r="9" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="90" cy="66" r="12" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90" y="70.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k</text>
<circle cx="250" cy="66" r="12" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="70.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t</text>
<circle cx="90" cy="110" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="90" y="114.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<circle cx="210" cy="110" r="12" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="210" y="114.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">i</text>
<circle cx="290" cy="110" r="12" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="114.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<circle cx="186" cy="154" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="186" y="158.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">m</text>
<circle cx="234" cy="154" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="234" y="158.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p</text>
<circle cx="290" cy="154" r="12" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="290" y="158.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p</text>
<text x="8" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">词典</text>
<text x="170" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">沿边逐字节走: 查 tip 只走 3 步</text>
</svg>
```

**细节。**

- FST 要求词按序输入，建出的是最小自动机。
- 查询时一个字节一个字节地沿边走，代价只与词长有关，与词的个数无关。

**为什么。** 比排序数组少了整词比较，比哈希表多了有序性，能做前缀查找。

**例题：** LC 208 实现 Trie (前缀树)

实现前缀树 `Trie`：`insert(word)` 插入单词；`search(word)` 单词已插入则返回 `true`；`startsWith(prefix)` 有已插入的单词以 `prefix` 开头则返回 `true`。

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
