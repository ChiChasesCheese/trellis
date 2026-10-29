---
id: uth-ai-prefix-cache-1-radix-tree
node: ai.prefix-cache
type: qa
step: 1
---
## Q
**相同开头别重算：基数树**｜SGLang · RadixAttention

成百上千个请求都以同一段系统提示词开头，模型要把这段开头的 KV 缓存重复算吗？怎样快速找出「已经算过的最长开头」？

## A
**背景。** 一个 token 的 KV 只取决于它自己和前面的 token，所以两个请求开头相同，这段的 KV 就相同，可以共用。难点：新请求来了，怎样在一大堆已缓存的序列里找到和它共同开头最长的那条？逐条比太慢；整条序列当哈希键，又只能匹配「完全相同」。

**结构。** 基数树（radix tree）：前缀树（trie）的压缩版，每条边是一段 token，节点挂着这段的 KV 缓存。从根出发，沿着与新请求相同的边往下走，走到的深度就是命中长度；只匹配半条边时，在分叉处把边劈成两条。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<circle cx="170" cy="20" r="9" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="170" y="24" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">根</text>
<rect x="20" y="56" width="150" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="95" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">系统提示</text>
<rect x="215" y="56" width="110" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="270" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">另一个提示</text>
<line x1="165" y1="28" x2="95" y2="56" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="175" y1="28" x2="270" y2="56" stroke="currentColor" stroke-width="1"/>
<rect x="12" y="116" width="80" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="52" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">问题 1</text>
<rect x="104" y="116" width="80" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="144" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">问题 2</text>
<rect x="230" y="116" width="80" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="270" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">问题 3</text>
<line x1="80" y1="84" x2="52" y2="116" stroke="currentColor" stroke-width="1"/>
<line x1="110" y1="84" x2="144" y2="116" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="270" y1="84" x2="270" y2="116" stroke="currentColor" stroke-width="1"/>
<text x="170" y="166" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">蓝线: 新请求(系统提示 + 问题 2)命中</text>
<text x="170" y="184" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚线: 最久没用的叶子, 先淘汰</text>
<text x="170" y="202" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每条边是一段 token, 共同开头只存一份</text>
</svg>
```

**细节。**

- 节点用字典存孩子，键是边上的第一个 token
- 请求运行期间，路径上的节点 `lock_ref` 大于 0，不会被淘汰
- 默认淘汰策略是 LRU：只淘汰叶子，叶子没了父节点才变成叶子

**为什么。** 没有分叉的长链压成一条边，比 trie 一个节点一个 token 更省空间。

**例题：** LC 208 实现 Trie（前缀树）（同类：LC 211 添加与搜索单词）

实现前缀树：`insert(word)` 插入单词，`search(word)` 判断单词是否存在，`startsWith(prefix)` 判断是否有单词以 `prefix` 开头。例：`insert("apple")` 后，`search("app")` → `false`，`startsWith("app")` → `true`。基数树把这里的单字符边合并成了长边。

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
