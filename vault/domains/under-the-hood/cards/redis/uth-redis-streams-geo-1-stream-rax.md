---
id: uth-redis-streams-geo-1-stream-rax
node: redis.streams-geo
type: qa
step: 1
---
## Q
**Stream 里的消息怎么存**｜Redis · 8.10

Redis Stream 的 `XADD` 追加消息、`XRANGE` 按 ID 范围读，底下是什么结构？

## A
**背景。** Stream 是只追加的消息日志，每条消息有个递增的 ID。要快速追加，也要按 ID 范围读。基数树（radix tree）是按“前缀”分路的树：ID 前几位相同的消息走同一条路，所以相邻的 ID 在树里也挨在一起。

**结构。** 基数树，键是 128 位的消息 ID，值是一个 listpack，每个 listpack 装一批消息。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">键 = 128 位消息 ID (毫秒 + 序号), 值 = 一批消息</text>
<rect x="120" y="26" width="100" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="170" y="41.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">基数树 (radix)</text>
<line x1="170" y1="50" x2="55" y2="90" stroke="currentColor" stroke-width="1"/>
<polygon points="55,90 59.8,85.5 61.6,90.6" fill="currentColor"/>
<rect x="10" y="90" width="94" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="57" y="107" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">17000-0</text>
<text x="57" y="123" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">listpack</text>
<line x1="170" y1="50" x2="163" y2="90" stroke="currentColor" stroke-width="1"/>
<polygon points="163,90 161.4,83.6 166.7,84.6" fill="currentColor"/>
<rect x="118" y="90" width="94" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="165" y="107" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">17050-0</text>
<text x="165" y="123" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">listpack</text>
<line x1="170" y1="50" x2="271" y2="90" stroke="currentColor" stroke-width="1"/>
<polygon points="271,90 264.4,90.3 266.4,85.3" fill="currentColor"/>
<rect x="226" y="90" width="94" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="273" y="107" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">17120-0</text>
<text x="273" y="123" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">listpack</text>
<text x="8" y="154" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">ID 按大端编码, 树里的字典序就是时间顺序</text>
<text x="8" y="172" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">一个 listpack 默认最多 100 条或 4096 字节, 满了开新节点</text>
<text x="8" y="190" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">追加只动最后一个节点; 范围读先定位, 再顺序扫</text>
</svg>
```

**细节。**

- ID = 毫秒时间戳 + 序号，各 64 位，按大端编码，所以树里的字典序就是时间顺序
- 一个 listpack 默认最多 100 条消息或 4096 字节，满了开新节点
- 追加只动最后一个节点；按 ID 范围读，先在树里定位再顺序扫 listpack

**为什么。** 一条消息一个树节点太费内存，整条流一个 listpack 又没法快速定位；一批一个节点是折中。

**例题：** LC 208 实现 Trie（前缀树）

实现前缀树：`insert(word)` 插入单词，`search(word)` 判断单词是否存在，`startsWith(prefix)` 判断是否有单词以它为前缀。例：插入 `apple` 后，`search("app")` → `false`，`startsWith("app")` → `true`。前缀相同的单词共用同一条路径，和基数树一样。

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
